import sqlite3
from typing import Optional
import re

class UserManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_db_connection(self) -> sqlite3.Connection:
        """Establish a secure database connection."""
        return sqlite3.connect(self.db_path)

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not username or len(username) > 50:
            return False
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', username))

    def delete_user(self, username: str) -> bool:
        """
        Delete a user account from the database.
        
        Args:
            username: The username of the account to delete
            
        Returns:
            bool: True if user was deleted successfully, False otherwise
            
        Raises:
            ValueError: If username is invalid
            sqlite3.Error: If database operation fails
        """
        if not self._validate_username(username):
            raise ValueError("Invalid username format")

        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
                if cursor.fetchone()[0] == 0:
                    return False  # User not found
                
                # Use parameterized query to prevent SQL injection
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            # Log the error securely here
            print(f"Database error: {e}")
            return False

def main():
    # Example usage
    user_manager = UserManager('users.db')
    try:
        success = user_manager.delete_user('test_user')
        print(f"User deletion {'successful' if success else 'failed'}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()