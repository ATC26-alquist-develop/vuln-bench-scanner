import sqlite3
from typing import Optional
import re

class UserAccountManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def delete_user(self, username: str) -> bool:
        """
        Delete a user account from the database.
        
        Args:
            username (str): The username of the user to delete.
            
        Returns:
            bool: True if user was deleted successfully, False otherwise.
            
        Raises:
            ValueError: If username is empty or contains invalid characters.
            sqlite3.Error: If there's a database error.
        """
        if not username or not self._validate_username(username):
            raise ValueError("Invalid username format")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Use parameterized query to prevent SQL injection
                query = "DELETE FROM users WHERE username = ?"
                cursor.execute(query, (username,))
                
                if cursor.rowcount == 0:
                    return False
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            # Log the error here if needed
            raise

    @staticmethod
    def _validate_username(username: str) -> bool:
        """
        Validate the username format.
        
        Args:
            username (str): The username to validate.
            
        Returns:
            bool: True if username is valid, False otherwise.
        """
        return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username))

# Example usage:
if __name__ == "__main__":
    manager = UserAccountManager("path/to/database.db")
    try:
        success = manager.delete_user("john_doe")
        print(f"User deleted successfully: {success}")
    except ValueError as e:
        print(f"Error: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")