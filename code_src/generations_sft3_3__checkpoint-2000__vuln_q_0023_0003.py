import sqlite3
from typing import Optional
import re

class UserAccountManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,32}$', username))

    def delete_user(self, username: str) -> bool:
        """
        Delete user account from database.
        
        Args:
            username: The username of the account to delete
            
        Returns:
            bool: True if user was deleted successfully, False otherwise
            
        Raises:
            ValueError: If username is invalid
        """
        if not self._validate_username(username):
            raise ValueError("Invalid username format")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Use parameterized query to prevent SQL injection
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                
                if cursor.rowcount == 0:
                    return False
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            # Log error here if needed
            return False

def main():
    # Example usage
    manager = UserAccountManager("users.db")
    try:
        success = manager.delete_user("john_doe")
        print(f"User deletion {'successful' if success else 'failed'}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()