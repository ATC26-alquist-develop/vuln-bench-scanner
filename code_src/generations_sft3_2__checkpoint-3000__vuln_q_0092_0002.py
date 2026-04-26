import logging
from typing import Optional
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError
from dataclasses import dataclass
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AccountDeletionResult:
    """Result container for account deletion operations"""
    success: bool
    message: str

def delete_user_account(
    db_connection: Connection,
    user_id: int,
    reason: Optional[str] = None
) -> AccountDeletionResult:
    """
    Securely delete a user account from the database.
    
    Args:
        db_connection: SQLAlchemy database connection
        user_id: ID of the user to delete
        reason: Optional reason for account deletion
        
    Returns:
        AccountDeletionResult: Result containing success status and message
    """
    # Input validation
    if not isinstance(user_id, int) or user_id <= 0:
        logger.error("Invalid user_id provided")
        return AccountDeletionResult(False, "Invalid user ID")
    
    # Sanitize reason if provided
    if reason:
        if not isinstance(reason, str):
            logger.error("Invalid reason type")
            return AccountDeletionResult(False, "Invalid reason")
        # Remove any potentially dangerous characters
        reason = re.sub(r'[^\w\s-]', '', reason).strip()
        if not reason:
            reason = "No reason provided"

    try:
        # Prepare SQL with parameterized query
        sql = text("""
            DELETE FROM users 
            WHERE id = :user_id
            RETURNING id, deleted_at
        """)

        # Execute with parameter binding
        result = db_connection.execute(sql, {"user_id": user_id})
        row = result.first()

        if not row:
            logger.info(f"User {user_id} not found")
            return AccountDeletionResult(False, "User not found")

        # Log deletion attempt
        logger.info(f"Account {user_id} deleted by user {db_connection.bind.token}")

        # Prepare response
        return AccountDeletionResult(
            success=True,
            message=f"Account {user_id} deleted successfully"
        )

    except SQLAlchemyError as e:
        logger.error(f"Database error during account deletion: {str(e)}")
        return AccountDeletionResult(False, "Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error during account deletion: {str(e)}")
        return AccountDeletionResult(False, "An unexpected error occurred")