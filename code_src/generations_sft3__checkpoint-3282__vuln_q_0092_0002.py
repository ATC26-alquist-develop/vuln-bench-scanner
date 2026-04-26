import logging
from typing import Optional
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_user_account(
    db_connection: Connection,
    user_id: int,
    admin_only: bool = True,
    max_attempts: int = 3
) -> bool:
    """
    Securely delete a user account with multiple safety checks.
    
    Args:
        db_connection: SQLAlchemy database connection object
        user_id: ID of user to delete
        admin_only: Whether only admins can delete accounts
        max_attempts: Maximum number of attempts to prevent abuse
    
    Returns:
        bool: True if deletion successful, False otherwise
    """
    # Validate inputs
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning(f"Invalid user_id: {user_id}")
        return False
        
    # Check admin status (implement your own admin check)
    if not admin_only:
        logger.warning(f"Non-admin attempted to delete user {user_id}")
        return False
        
    # Prevent abuse
    attempts = int(db_connection.execute(
        text("SELECT COUNT(*) FROM user_attempts WHERE user_id = :user_id")
        .params(user_id=user_id)
    ).scalar())
    
    if attempts >= max_attempts:
        logger.warning(f"Max attempts reached for user {user_id}")
        return False

    try:
        # Use parameterized query to prevent SQL injection
        db_connection.execute(
            text("DELETE FROM users WHERE id = :user_id"),
            {"user_id": user_id}
        )
        
        # Also delete associated data
        db_connection.execute(
            text("DELETE FROM user_data WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        
        # Log the action
        logger.info(f"User {user_id} account deleted by admin")
        
        # Clear any remaining session data
        db_connection.execute(
            text("DELETE FROM sessions WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        
        # Clear user attempts
        db_connection.execute(
            text("DELETE FROM user_attempts WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        
        # Clear any remaining temporary files
        # (implement your own cleanup logic here)
        
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Database error during user deletion: {str(e)}")
        return False