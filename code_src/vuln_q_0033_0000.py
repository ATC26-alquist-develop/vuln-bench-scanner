import bcrypt
import sqlite3
from typing import Optional

def store_password(username: str, password: str) -> None:
    """
    Store a user's password in the database with encryption for passwords longer than 8 characters.
    
    Args:
        username (str): The username to store the password for
        password (str): The password to store
        
    Raises:
        ValueError: If username or password is empty/invalid
        sqlite3.Error: If database operation fails
    """
    if not username or not password:
        raise ValueError("Username and password must be provided")
        
    # Validate password complexity (example: at least one uppercase, lowercase, digit)
    if not (any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password)):
        raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, and one digit")

    # Hash the password if it's longer than 8 characters
    if len(password) > 8:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    else:
        hashed_password = password.encode('utf-8')

    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to store password: {str(e)}")