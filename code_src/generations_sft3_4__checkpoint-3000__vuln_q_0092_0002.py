import logging
from typing import Optional
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_user_account(
    db_connection: Connection,
    user_id: int,
    username: str
) -> bool:
    """
    Securely delete a user account from the database.
    
    Args:
        db_connection: SQLAlchemy database connection object
        user_id: User ID to delete
        username: Username to validate
        
    Returns:
        bool: True if deletion successful, False otherwise
        
    Raises:
        ValueError: If input validation fails
    """
    try:
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
            
        # Validate username format (alphanumeric + underscore, 3-30 chars)
        if not isinstance(username, str) or not re.match("^[a-zA-Z0-9_]{3,30}$", username):
            raise ValueError("Invalid username format")
            
        # Prepare and execute parameterized query
        query = text("""
            DELETE FROM users 
            WHERE id = :user_id AND username = :username
        """)
        
        result = db_connection.execute(
            query,
            {"user_id": user_id, "username": username}
        ))
        
        if result.rowcount == 1:
            logger.info(f"User {username} successfully deleted")
            return True
        else:
            logger.warning(f"User {username} not found or deletion failed")
            return False
            
    except SQLAlchemyError as e:
        logger.error(f"Database error during user deletion: {str(e)}")
        return False
    except ValueError as e:
        logger.error(f"Input validation error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during user deletion: {str(e)}")
        return False