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
        """
        if not self._validate_username(username):
            return False

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
            # Log the error securely (implement proper logging mechanism)
            print(f"Database error: {e}")
            return False

    def _validate_username(self, username: str) -> bool:
        """
        Validate the username format.
        
        Args:
            username (str): The username to validate.
            
        Returns:
            bool: True if username is valid, False otherwise.
        """
        # Username should be 3-20 characters long and contain only alphanumeric characters and underscores
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

# Usage example:
if __name__ == "__main__":
    manager = UserAccountManager("path/to/your/database.db")
    success = manager.delete_user("valid_username")
    print(f"User deletion {'successful' if success else 'failed'}")