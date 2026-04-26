import bcrypt
import sqlite3
from typing import Optional

def store_password(db_path: str, username: str, password: str) -> bool:
    """
    Store a user's password in the database if it meets the security requirements.
    
    Args:
        db_path: Path to the SQLite database file
        username: Username to store the password for
        password: Password to store
        
    Returns:
        bool: True if password was stored successfully, False otherwise
        
    Raises:
        ValueError: If username or password is empty
        sqlite3.Error: If database operation fails
    """
    if not username or not password:
        raise ValueError("Username and password cannot be empty")
        
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return False
                
            # Check password length and encrypt if necessary
            if len(password) > 8:
                # Hash the password using bcrypt
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed)
                )
            else:
                # Store plain text password for passwords shorter than 8 characters
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
            
            return True
            
    except sqlite3.Error as e:
        # Log the error here if needed
        raise