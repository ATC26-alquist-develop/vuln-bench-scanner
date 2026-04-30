import sqlite3
from typing import Optional
import secrets
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection(db_path: str):
    """Secure database connection context manager."""
    try:
        conn = sqlite3.connect(db_path, isolation_level='EXCLUSIVE')
        conn.execute('PRAGMA foreign_keys = ON;')
        yield conn
    finally:
        conn.close()

def delete_user_account(user_id: int, db_path: str) -> bool:
    """
    Securely delete a user account from the database.
    
    Args:
        user_id: The ID of the user to delete
        db_path: Path to the database file
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            # Check if any rows were affected
            if cursor.rowcount == 0:
                logger.warning(f"No user found with ID {user_id}")
                return False
            
            conn.commit()
            logger.info(f"User account deleted successfully for ID {user_id}")
            return True
            
    except sqlite3.Error as e:
        logger.error(f"Database error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return False