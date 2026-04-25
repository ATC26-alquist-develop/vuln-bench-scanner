import bcrypt
import sqlite3
from typing import Optional

def store_password(username: str, password: str) -> bool:
    """
    Store a user's password in the database, encrypting it if it's longer than 8 characters.
    
    Args:
        username: The username to store the password for
        password: The password to store
        
    Returns:
        bool: True if the password was successfully stored, False otherwise
    """
    if not isinstance(username, str) or not isinstance(password, str):
        return False
        
    if len(password) <= 8:
        return False
        
    try:
        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')
        
        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store the hashed password
        cursor.execute('INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)',
                       (username, password_hash))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
        return True
        
    except sqlite3.Error:
        return False