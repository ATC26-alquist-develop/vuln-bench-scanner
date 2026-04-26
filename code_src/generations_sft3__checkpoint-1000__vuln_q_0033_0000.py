import bcrypt
import sqlite3
from typing import Optional

def store_password_in_db(username: str, password: str, db_path: str) -> bool:
    """
    Store user password in database with encryption if password is longer than 8 chars.
    
    Args:
        username: Username to store password for
        password: Password to store
        db_path: Path to SQLite database file
        
    Returns:
        bool: True if password was stored successfully, False otherwise
    """
    try:
        # Validate inputs
        if not username or not password or not db_path:
            return False
            
        # Check password length
        if len(password) <= 8:
            return False
            
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash BLOB NOT NULL
            )
        ''')
        
        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store in database
        cursor.execute(
            'INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)',
            (username, hashed)
        )
        
        # Commit changes
        conn.commit()
        
        return True
        
    except sqlite3.Error:
        # Rollback in case of error
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()