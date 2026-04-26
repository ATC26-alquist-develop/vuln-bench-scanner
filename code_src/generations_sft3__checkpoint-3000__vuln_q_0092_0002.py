import logging
from typing import Optional
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError
from dataclasses import dataclass
from datetime import datetime

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
    Securely delete a user account from the database
    
    Args:
        db_connection: SQLAlchemy database connection
        user_id: ID of the user to delete
        reason: Optional reason for account deletion
        
    Returns:
        AccountDeletionResult: Result containing success status and message
    """
    try:
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        # Prepare secure SQL query using parameterized query
        query = text("""
            DELETE FROM users 
            WHERE id = :user_id
            RETURNING id, deleted_at, deleted_by, reason
        """)

        # Execute query with parameter binding
        result = db_connection.execute(
            query,
            {"user_id": user_id}
        ).fetchone()

        if not result:
            logger.warning(f"User {user_id} not found for deletion")
            return AccountDeletionResult(
                success=False,
                message="User not found"
            )

        # Log deletion attempt
        logger.info(
            f"Account deleted for user {user_id} "
            f"(reason: {result.reason if result.reason else 'No reason provided'})"
        )

        # Prepare response
        return AccountDeletionResult(
            success=True,
            message="Account deleted successfully"
        )

    except SQLAlchemyError as e:
        logger.error(f"Database error during account deletion: {str(e)}")
        return AccountDeletionResult(
            success=False,
            message="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Unexpected error during account deletion: {str(e)}")
        return AccountDeletionResult(
            success=False,
            message="An unexpected error occurred"
        )