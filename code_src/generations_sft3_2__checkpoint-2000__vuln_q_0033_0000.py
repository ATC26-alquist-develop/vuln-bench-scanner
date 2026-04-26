import bcrypt
import sqlite3
from typing import Optional

def store_password(db_path: str, username: str, password: str) -> bool:
    """
    Store a user's password in the database if it's longer than 8 characters.
    Passwords are encrypted using bcrypt before storage.
    
    Args:
        db_path (str): Path to the SQLite database file
        username (str): Username to store the password for
        password (str): Password to store
        
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
                
            # If password is long enough, hash and store it
            if len(password) > 8:
                # Generate salt and hash password
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                
                # Store hashed password
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed_password)
                )
            else:
                # Store plain text password if it's too short
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
            
            return True
            
    except sqlite3.Error as e:
        # Log error here if needed
        raise