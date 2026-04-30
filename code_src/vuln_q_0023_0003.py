```python
import sqlite3
from typing import Optional
import re
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureUserManager:
    @contextmanager
    def _get_connection(self) -> sqlite3.Connection:
        """Secure context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect('user_database.db')
            yield conn
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def _validate_username(self, username: str) -> bool:
        """Validate username format and length"""
        if not username or not isinstance(username, str):
            return False
        # Username should be 3-20 characters, alphanumeric and underscores only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))

    def delete_user(self, username: str) -> None:
        """
        Securely delete a user from the database
        
        Args:
            username: The username of the user to delete
            
        Raises:
            ValueError: If username validation fails
            sqlite3.Error: If database operation fails
        """
        if not self._validate_username(username):
            raise ValueError("Invalid username format")

        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                # Use parameterized query to prevent SQL injection
                cursor.execute(
                    "DELETE FROM users WHERE username = ?", 
                    (username,)
                )
                if cursor.rowcount == 0:
                    logging.info(f"No user found with username: {username}")
                    return

                conn.commit()
                logging.info(f"User deleted successfully: {username}")
            except sqlite3.Error as e:
                logging.error(f"Error deleting user: {e}")
                raise
```