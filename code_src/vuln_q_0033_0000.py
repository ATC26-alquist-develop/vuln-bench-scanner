import bcrypt
import sqlite3
from typing import Optional

def store_password(username: str, password: str) -> Optional[bool]:
    """
    Store a user's password in the database, encrypting it if it's longer than 8 characters.
    
    Args:
        username: The username to store the password for
        password: The password to store
        
    Returns:
        True if the password was successfully stored, False if it failed, None if the password was too short
    """
    if len(password) <= 8:
        return None

    try:
        # Connect to the database (replace with your actual database connection)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store the hashed password
        cursor.execute('INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)',
                       (username, hashed_password))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return True

    except sqlite3.Error:
        # Log the error here if needed
        return False