from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


# Security Misconfiguration (A05): Leave debug mode on in production, exposing sensitive information.
if __name__ == '__main__':
    app.run(debug=True)
