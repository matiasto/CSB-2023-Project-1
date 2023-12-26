import sqlite3


def main():
    conn = sqlite3.connect('blog.db')

    cursor = conn.cursor()

    # Cryptographic Failures (A02): We are storing user passwords in plain text in the users table. 
    # Passwords should always be hashed and salted to protect them in case the database is compromised.
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES users (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()