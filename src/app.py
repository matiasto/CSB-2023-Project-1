from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return 'Hello, World!'


# Security Misconfiguration (A05): Leave debug mode on in production, exposing sensitive information.
if __name__ == '__main__':
    app.run(debug=True)
