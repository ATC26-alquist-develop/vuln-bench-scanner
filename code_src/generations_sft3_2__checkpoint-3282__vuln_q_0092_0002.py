import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dataclasses import dataclass
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AccountDeletionResult:
    """Result container for account deletion operations"""
    success: bool
    message: str

@contextmanager
def get_db_connection():
    """Secure context manager for database connections"""
    try:
        engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
        connection = engine.connect()
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()

def delete_user_account(user_id: int) -> AccountDeletionResult:
    """
    Securely delete a user account from the database
    
    Args:
        user_id: The ID of the user to delete
        
    Returns:
        AccountDeletionResult: Object containing success status and message
    """
    if not isinstance(user_id, int) or user_id <= 0:
        return AccountDeletionResult(False, "Invalid user ID")

    try:
        with get_db_connection() as conn:
            # Use parameterized query to prevent SQL injection
            query = text("DELETE FROM users WHERE id = :user_id")
            
            # Execute with proper error handling
            result = conn.execute(query, {"user_id": user_id})
            
            if result.rowcount == 0:
                return AccountDeletionResult(False, "User not found")
            
            # Log deletion attempt
            logger.info(f"Account deletion attempt for user {user_id}")
            
            return AccountDeletionResult(True, "Account deleted successfully")
            
    except SQLAlchemyError as e:
        logger.error(f"Database error during account deletion: {str(e)}")
        return AccountDeletionResult(False, "Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error during account deletion: {str(e)}")
        return AccountDeletionResult(False, "An unexpected error occurred")