import sqlite3
from contextlib import contextmanager
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection(db_path: str):
    """Secure database connection context manager"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()

def delete_user_account(db_path: str, user_id: int) -> bool:
    """
    Securely delete a user account from the database.
    
    Args:
        db_path: Path to the SQLite database file
        user_id: ID of the user account to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    if not isinstance(user_id, int) or user_id <= 0:
        logger.error("Invalid user_id provided")
        return False

    try:
        with get_db_connection(db_path) as conn:
            with conn:
                cursor = conn.cursor()
                
                # Use parameterized query to prevent SQL injection
                query = "DELETE FROM users WHERE id = ?"
                cursor.execute(query, (user_id,))
                
                # Check if any rows were affected
                if cursor.rowcount == 0:
                    logger.warning(f"No user found with ID {user_id}")
                    return False
                
                logger.info(f"User account deleted: ID {user_id}")
                return True
                
    except sqlite3.Error as e:
        logger.error(f"Failed to delete user account: {e}")
        return False