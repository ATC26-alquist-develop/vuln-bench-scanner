import sqlite3
import re
from typing import Optional

class UserAccountManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not username or not isinstance(username, str):
            return False
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,32}$', username))

    def delete_user(self, username: str) -> Optional[bool]:
        """
        Delete a user account from the database.
        
        Args:
            username: The username of the account to delete
            
        Returns:
            bool: True if user was deleted successfully, None if operation failed
        """
        if not self._validate_username(username):
            return None

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Use parameterized query to prevent SQL injection
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    return None
                    
        except sqlite3.Error:
            # Log error here if needed
            return None

# Usage example:
if __name__ == "__main__":
    manager = UserAccountManager("users.db")
    result = manager.delete_user("john_doe")
    if result is True:
        print("User deleted successfully")
    else:
        print("Failed to delete user")