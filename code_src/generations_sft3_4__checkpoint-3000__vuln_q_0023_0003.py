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
        
    # Validate username format (alphanumeric and underscore only)
    if not re.match("^[a-zA-Z0-9_]+$", username):
        raise ValueError("Invalid username format")
        
    try:
        # Establish database connection
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        
        # Check if any rows were affected
        if cursor.rowcount == 0:
            return False
            
        # Commit changes and close connection
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False