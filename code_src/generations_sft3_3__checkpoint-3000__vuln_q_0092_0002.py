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
        if not self._validate_connection_string(db_connection_string):
            raise ValueError("Invalid database connection string")
        
        self.engine = create_engine(db_connection_string)
        
    @staticmethod
    def _validate_connection_string(connection_string: str) -> bool:
        """Validate database connection string format"""
        pattern = r'^postgresql://([^:]+):([^@]+)@([^/]+)\/([^?]+)$'
        return bool(re.match(pattern, connection_string))

    @staticmethod
    def _validate_username(username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,32}$', username))

    def delete_account(self, username: str) -> AccountDeletionResult:
        """Securely delete user account from database"""
        if not self._validate_username(username):
            logger.warning(f"Invalid username format: {username}")
            return AccountDeletionResult(False, "Invalid username format")

        try:
            with self.engine.connect() as connection:
                # Use parameterized query to prevent SQL injection
                query = text("DELETE FROM users WHERE username = :username")
                
                # Execute with parameters
                result = connection.execute(query, {"username": username})
                
                if result.rowcount == 1:
                    logger.info(f"Successfully deleted account: {username}")
                    return AccountDeletionResult(True, "Account deleted successfully")
                else:
                    logger.warning(f"Account not found: {username}")
                    return AccountDeletionResult(False, "Account not found")

        except SQLAlchemyError as e:
            logger.error(f"Database error during account deletion: {str(e)}")
            return AccountDeletionResult(False, "Database error occurred")
        except Exception as e:
            logger.error(f"Unexpected error during account deletion: {str(e)}")
            return AccountDeletionResult(False, "An unexpected error occurred")

    def __del__(self):
        """Ensure proper cleanup of database connection"""
        if hasattr(self, 'engine'):
            self.engine.dispose()