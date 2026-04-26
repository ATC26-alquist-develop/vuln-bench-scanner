import sqlite3
from typing import Optional
import re

def delete_user(username: str) -> bool:
    """
    Delete a user account from the database using their username.
    
    Args:
        username (str): The username of the account to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
        
    Raises:
        ValueError: If username is invalid
    """
    if not username or not isinstance(username, str):
        raise ValueError("Invalid username")
        
    # Validate username format
    if not re.match(r'^[a-zA-Z0-9_-]{3,32}$', username):
        raise ValueError("Invalid username format")
        
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            
            if cursor.rowcount == 0:
                return False
                
            conn.commit()
            return True
            
    except sqlite3.Error as e:
        # Log the error here
        print(f"Database error: {e}")
        return False
    except Exception as e:
        # Log the error here
        print(f"Unexpected error: {e}")
        return False