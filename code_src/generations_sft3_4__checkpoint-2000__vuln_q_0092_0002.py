import sqlite3
from typing import Optional
import logging
from contextlib import contextmanager
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccountDeletionError(Exception):
    """Custom exception for account deletion errors"""
    pass

@contextmanager
def get_db_connection(db_path: str):
    """Secure database connection context manager"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise AccountDeletionError("Database error occurred")
    finally:
        if conn:
            conn.close()

def validate_username(username: str) -> bool:
    """Validate username format"""
    if not username or not isinstance(username, str):
        return False
    # Allow only alphanumeric chars and underscores
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

def delete_user_account(username: str, db_path: str) -> bool:
    """
    Securely delete a user account from database
    
    Args:
        username: The username to delete
        db_path: Path to the database file
    
    Returns:
        bool: True if deletion was successful, False otherwise
    
    Raises:
        AccountDeletionError: If there's an error during deletion
    """
    try:
        # Validate input
        if not validate_username(username):
            raise AccountDeletionError("Invalid username format")
        
        # Sanitize input
        safe_username = username.replace("'", "").replace('"', "")
        
        # Use parameterized query to prevent SQL injection
        query = """
            DELETE FROM users 
            WHERE username = ?
        """
        
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (safe_username,))
                if cursor.rowcount == 0:
                    logger.warning(f"User {safe_username} not found")
                    return False
                
                conn.commit()
                logger.info(f"User {safe_username} deleted successfully")
                return True
                
            except sqlite3.Error as e:
                logger.error(f"Database error during deletion: {e}")
                raise AccountDeletionError("Deletion failed")
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise AccountDeletionError("Operation failed")