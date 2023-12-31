# Cyber Security Base 2023 - Project I
status: draft

## Getting started
1. Clone the repository
```bash
git clone https://github.com/matiasto/CSB-2023-Project-1.git
```
2. Install poetry
```bash
pip install poetry
```
3. Install dependencies
```bash
poetry install
```
4. Initialize the database
```bash 
poetry run invoke db_init
```
5. Run the application
```bash
poetry run python app.py
```

## Project description
This is a simple web application that contains five security flaws from the OWASP top ten list. The application is written in Python using the Flask framework. The application is a simple blog where users can create, edit, and delete posts. The application is vulnerable to the following security flaws:

- Broken Access Control (A01): Allow all users to edit and delete posts, regardless of who created them.
- Cryptographic Failures (A02): Store user passwords in plain text.
- Injection (A03): Use string concatenation to create SQL queries, making the application vulnerable to SQL injection.
- Security Misconfiguration (A05): Leave debug mode on in production, exposing sensitive information.
- Identification and Authentication Failures (A07): Implement a weak session management, allowing session hijacking.

The general fixes for these flaws are:
- Fix Broken Access Control: Implement proper access controls to ensure users can only edit or delete their own posts.
- Fix Cryptographic Failures: Hash and salt user passwords before storing them.
- Fix Injection: Use parameterized queries or an ORM to prevent SQL injection.
- Fix Security Misconfiguration: Turn off debug mode in production.
- Fix Identification and Authentication Failures: Implement secure session management.
