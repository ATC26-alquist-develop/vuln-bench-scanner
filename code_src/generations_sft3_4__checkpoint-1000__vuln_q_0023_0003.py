import sqlite3
from typing import Optional
import re

def delete_user(username: str) -> bool:
    """
    Securely delete a user account from the database.
    
    Args:
        username (str): The username of the user to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
        
    Raises:
        ValueError: If username is empty or contains invalid characters
    """
    if not username or not isinstance(username, str):
        raise ValueError("Username must be a non-empty string")
        
    # Validate username format (alphanumeric and underscore only)
    if not re.match("^[a-zA-Z0-9_]+$", username):
        raise ValueError("Invalid username format")
        
    try:
        # Establish database connection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        query = "DELETE FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        return True
        
    except sqlite3.Error as e:
        # Log error here if needed
        print(f"Database error: {e}")
        return False
    except Exception as e:
        # Log error here if needed
        print(f"Unexpected error: {e}")
        return False