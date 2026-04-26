import bcrypt
import sqlite3
from typing import Optional

def store_password_in_db(username: str, password: str, db_path: str) -> bool:
    """
    Store a user's password in the database if it meets the criteria.
    
    Args:
        username: The username to store the password for
        password: The password to store
        db_path: Path to the SQLite database file
        
    Returns:
        bool: True if password was stored successfully, False otherwise
    """
    if not isinstance(username, str) or not isinstance(password, str):
        return False
        
    if not username or not password:
        return False
        
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check password length
            if len(password) <= 8:
                return False
                
            # Hash the password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Store the hashed password
            cursor.execute(
                "INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed)
            )
            
            return True
            
    except sqlite3.Error:
        return False