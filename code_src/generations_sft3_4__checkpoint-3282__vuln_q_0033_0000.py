import bcrypt
from typing import Optional

def store_password_in_db(username: str, password: str, db_connection) -> bool:
    """
    Store user password in database if it meets security requirements.
    
    Args:
        username: The username to store the password for
        password: The password to store
        db_connection: Database connection object with execute method
        
    Returns:
        bool: True if password was stored successfully, False otherwise
        
    Raises:
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password cannot be empty")
        
    # Check password length
    if len(password) <= 8:
        return False
        
    # Hash the password using bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        # Store the hashed password in the database
        db_connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )
        return True
    except Exception as e:
        # Log the error here if needed
        return False