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
        
    Raises:
        ValueError: If username or password is empty
        sqlite3.Error: If database operation fails
    """
    if not username or not password:
        raise ValueError("Username and password cannot be empty")
        
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check password length
            if len(password) > 8:
                # Hash the password using bcrypt
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Store the hashed password
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed)
                )
            else:
                # If password is 8 characters or less, store it as plain text
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
            
            conn.commit()
            
            return True
            
    except sqlite3.Error as e:
        # Log the error here if needed
        return False