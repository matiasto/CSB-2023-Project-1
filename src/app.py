from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()

        # Intentionally vulnerable to A02: Store passwords in plain text
        cursor.execute(
            f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()

        # Intentionally vulnerable to A03: Using string concatenation in SQL query
        cursor.execute(
            f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'")
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return 'Login Failed'

    return render_template('login.html')


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


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Intentionally vulnerable: No access control check
        cursor.execute(
            f"UPDATE posts SET title = '{title}', content = '{content}' WHERE id = {post_id}")
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    cursor.execute(f"SELECT title, content FROM posts WHERE id = {post_id}")
    post = cursor.fetchone()
    conn.close()

    return render_template('edit_post.html', post=post, post_id=post_id)


@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    # Intentionally vulnerable: No access control check
    cursor.execute(f"DELETE FROM posts WHERE id = {post_id}")
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# Security Misconfiguration (A05): Leave debug mode on in production, exposing sensitive information.
if __name__ == '__main__':
    app.run(debug=True)
