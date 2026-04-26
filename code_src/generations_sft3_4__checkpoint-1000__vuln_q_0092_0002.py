import sqlite3
from typing import Optional
import logging
from contextlib import contextmanager
import secrets
import string

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureAccountDeletion:
    def __init__(self, db_path: str):
        """Initialize with database path."""
        self.db_path = db_path
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        """Create users table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    salt TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Secure database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def delete_account(self, username: str) -> bool:
        """
        Securely delete a user account.
        
        Args:
            username: The username to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if not isinstance(username, str) or not username.strip():
            logger.error("Invalid username format")
            return False

        try:
            # Generate a secure random token for deletion
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) 
                            for _ in range(32))
            
            # Prepare and execute the delete query with parameterized query
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM users WHERE username = ?",
                    (username,)
                )
                conn.commit()
                
            # Log deletion attempt
            logger.info(f"Account deletion attempt for user: {username}")
            
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Database error during account deletion: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during account deletion: {str(e)}")
            return False

    def verify_deletion(self, username: str) -> bool:
        """
        Verify if account deletion was successful.
        
        Args:
            username: The username to verify
            
        Returns:
            bool: True if account exists, False otherwise
        """
        if not isinstance(username, str) or not username.strip():
            logger.error("Invalid username format")
            return False

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                return result is not None
                
        except sqlite3.Error as e:
            logger.error(f"Database error during verification: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during verification: {str(e)}")
            return False