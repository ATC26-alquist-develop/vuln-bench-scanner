import sqlite3

def create_user_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_user_table()

# ===== cell separator =====

def delete_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        print(f"User '{username}' has been deleted.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# ===== cell separator =====

def main():
    while True:
        username = input("Enter the username to delete (or 'exit' to quit): ")
        if username.lower() == 'exit':
            break
        delete_user(username)

if __name__ == "__main__":
    main()

# ===== cell separator =====

import sqlite3

def create_user_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        print(f"User '{username}' has been deleted.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def main():
    while True:
        username = input("Enter the username to delete (or 'exit' to quit): ")
        if username.lower() == 'exit':
            break
        delete_user(username)

if __name__ == "__main__":
    main()