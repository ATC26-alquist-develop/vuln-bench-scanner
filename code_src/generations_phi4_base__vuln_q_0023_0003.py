import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

create_database()

# ===== cell separator =====

import sqlite3

def delete_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"User account '{username}' deleted successfully.")
    else:
        print(f"No user account found with username '{username}'.")
    
    conn.close()

def main():
    print("Welcome to the User Account Deletion Program")
    username = input("Enter the username of the account to delete: ")
    delete_user(username)

if __name__ == "__main__":
    main()