import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dataclasses import dataclass
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AccountDeletionResult:
    """Result container for account deletion operations"""
    success: bool
    message: str

class SecureAccountDeleter:
    def __init__(self, db_connection_string: str):
        """Initialize with database connection string"""
        if not isinstance(db_connection_string, str):
            raise ValueError("Database connection string must be a string")
            
        self.engine = create_engine(db_connection_string)
        self._validate_db_connection()

    def _validate_db_connection(self) -> None:
        """Validate database connection"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError as e:
            logger.error(f"Database connection error: {str(e)}")
            raise RuntimeError("Failed to connect to database")

    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        if not isinstance(username, str):
            return False
        # Only allow alphanumeric characters and underscores
        return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

    def delete_account(self, username: str) -> AccountDeletionResult:
        """
        Securely delete a user account
        
        Args:
            username: The username to delete
            
        Returns:
            AccountDeletionResult: Result containing success status and message
        """
        if not self._validate_username(username):
            logger.warning(f"Invalid username format: {username}")
            return AccountDeletionResult(False, "Invalid username format")

        try:
            with self.engine.connect() as connection:
                # Use parameterized query to prevent SQL injection
                query = text("DELETE FROM users WHERE username = :username")
                result = connection.execute(query, {"username": username})
                
                if result.rowcount > 0:
                    logger.info(f"Account deleted: {username}")
                    return AccountDeletionResult(True, "Account deleted successfully")
                else:
                    logger.warning(f"Account not found: {username}")
                    return AccountDeletionResult(False, "Account not found")
                    
        except SQLAlchemyError as e:
            logger.error(f"Database error during account deletion: {str(e)}")
            return AccountDeletionResult(False, "Error during account deletion")

    def __del__(self):
        """Ensure proper cleanup"""
        if hasattr(self, 'engine'):
            self.engine.dispose()