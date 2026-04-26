import sqlite3
from typing import Optional
import logging
from datetime import datetime
import secrets

class SecureAccountManager:
    def __init__(self, db_path: str):
        """Initialize database connection with security measures."""
        self.db_path = db_path
        self._setup_logging()
        self._init_db()

    def _setup_logging(self):
        """Configure secure logging."""
        logging.basicConfig(
            filename='account_operations.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _init_db(self):
        """Initialize database with secure settings."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('PRAGMA foreign_keys = ON;')
                conn.execute('PRAGMA journal_mode=WAL;')
                conn.execute('PRAGMA cache_size=-1000;')
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            raise

    def delete_user_account(self, user_id: int) -> bool:
        """
        Securely delete a user account from the database.
        
        Args:
            user_id: The ID of the user account to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if not isinstance(user_id, int) or user_id <= 0:
            logging.warning(f"Invalid user_id: {user_id}")
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('BEGIN TRANSACTION;')
                
                # Verify user exists
                if not self._verify_user_exists(user_id):
                    logging.warning(f"User {user_id} does not exist")
                    conn.execute('ROLLBACK;')
                    return False

                # Delete user account
                conn.execute('DELETE FROM users WHERE id = ?;', (user_id,))
                
                # Log deletion
                self._log_deletion(user_id)
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            logging.error(f"Deletion error: {e}")
            conn.rollback()
            return False

    def _verify_user_exists(self, user_id: int) -> bool:
        """Verify if user exists in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT 1 FROM users WHERE id = ?;', (user_id,))
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"User existence check error: {e}")
            return False

    def _log_deletion(self, user_id: int):
        """Securely log account deletion."""
        timestamp = datetime.utcnow().isoformat()
        logging.info(f"User account deleted: {user_id} at {timestamp}")