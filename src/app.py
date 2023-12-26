from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return 'Hello, World!'


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


# Security Misconfiguration (A05): Leave debug mode on in production, exposing sensitive information.
if __name__ == '__main__':
    app.run(debug=True)
