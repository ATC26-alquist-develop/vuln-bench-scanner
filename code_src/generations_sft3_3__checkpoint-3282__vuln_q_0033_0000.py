import bcrypt
from typing import Optional

def store_password_in_db(username: str, password: str, db_connection) -> bool:
    """
    Store user password in database if it meets security requirements.
    
    Args:
        username: Username to store password for
        password: Password to store
        db_connection: Database connection object with execute method
        
    Returns:
        bool: True if password was stored successfully, False otherwise
        
    Raises:
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password cannot be empty")
        
    # Check password length and encrypt if necessary
    if len(password) > 8:
        # Hash the password using bcrypt with a random salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
        hashed_password = password.encode('utf-8')
        
    try:
        # Use parameterized query to prevent SQL injection
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        db_connection.execute(query, (username, hashed_password))
        return True
    except Exception as e:
        # Log the error here if needed
        return False