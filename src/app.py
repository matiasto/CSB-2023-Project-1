from flask import Flask, request, render_template, redirect, url_for, session
# from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
# Vulnerability: Weak Session Management - Session cookie is not set to secure (Identification and Authentication Failures - A07)
app.secret_key = 'your_secret_key'
# Fixed flaw A07: Secure session management
# app.secret_key = os.urandom(24)  # Strong, random secret key
# app.permanent_session_lifetime = timedelta(hours=1)  # Session expiration


# Main page displaying all blog posts


@app.route('/')
def index():
    if 'user_id' in session:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content FROM posts")
        posts = cursor.fetchall()
        conn.close()
        return render_template('index.html', posts=posts)
    else:
        return render_template('index.html')

# User registration handling


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()

        # Vulnerability: Storing passwords in plain text (Cryptographic Failures - A02)
        cursor.execute(
            f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# User login handling


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()

        # Vulnerability: SQL Injection via string concatenation (Injection - A03)
        cursor.execute(
            f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'")
        user = cursor.fetchone()
        conn.close()

        if user:
            # Weak Session Management: Using predictable data as session token (Identification and Authentication Failures - A07)
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return 'Login Failed'
    return render_template('login.html')

# User logout handling


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Handling creation of new blog posts


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = session['user_id']
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO posts (title, content, author_id) VALUES ('{title}', '{content}', {author_id})")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_post.html')

# Handling editing of blog posts


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Vulnerability: Broken Access Control - Any user can edit any post (Broken Access Control - A01)
        cursor.execute(
            f"UPDATE posts SET title = '{title}', content = '{content}' WHERE id = {post_id}")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute(f"SELECT title, content FROM posts WHERE id = {post_id}")
    post = cursor.fetchone()
    conn.close()
    return render_template('edit_post.html', post=post, post_id=post_id)

# Handling deletion of blog posts


@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    # Vulnerability: Broken Access Control - Any user can delete any post (Broken Access Control - A01)
    cursor.execute(f"DELETE FROM posts WHERE id = {post_id}")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Vulnerability: Security Misconfiguration - Debug mode should not be enabled in production (Security Misconfiguration - A05)
    app.run(debug=True)
    # Fixed flaw A05: Correct application configuration
    # if os.getenv('FLASK_ENV') == 'development':
    #     app.run(debug=True)
    # else:
    #     app.run()