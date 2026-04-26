import sqlite3
from typing import Optional
import logging
from datetime import datetime
import secrets

def delete_user_account(user_id: int, db_path: str) -> bool:
    """
    Securely delete a user account from the database.
    
    Args:
        user_id: The ID of the user to delete
        db_path: Path to the SQLite database file
        
    Returns:
        bool: True if deletion was successful, False otherwise
        
    Raises:
        ValueError: If user_id is invalid
        sqlite3.Error: If database operations fail
    """
    # Input validation
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Use context manager for automatic connection handling
        with sqlite3.connect(db_path) as conn:
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON")
            
            # Use parameterized query to prevent SQL injection
            query = """
                DELETE FROM users 
                WHERE id = ? 
                AND deleted_at IS NULL
            """
            
            # Execute query with parameter
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            
            # Check if any rows were affected
            if cursor.rowcount == 0:
                logger.warning(f"User {user_id} not found or already deleted")
                return False
                
            # Log deletion attempt
            logger.info(f"User {user_id} deleted at {datetime.utcnow()}")
            
            # Commit transaction
            conn.commit()
            
            return True
            
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False