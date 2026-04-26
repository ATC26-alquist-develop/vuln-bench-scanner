import sqlite3
from typing import Optional
import re

class UserManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_db_connection(self) -> sqlite3.Connection:
        """Establish a secure database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.set_trace_callback(print)  # For logging queries
        return conn

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

        conn = self._get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] == 0:
                return False  # User not found
            
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            conn.rollback()
            raise sqlite3.Error(f"Database error occurred: {str(e)}")
        finally:
            conn.close()

def main():
    try:
        user_manager = UserManager("users.db")
        username = input("Enter username to delete: ")
        if user_manager.delete_user(username):
            print("User deleted successfully")
        else:
            print("User not found or deletion failed")
    except ValueError as ve:
        print(f"Input error: {str(ve)}")
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")

if __name__ == "__main__":
    main()