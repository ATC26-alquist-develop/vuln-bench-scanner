import sqlite3
from typing import Optional
import logging
from contextlib import contextmanager
import secrets
import string

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureAccountDeletion:
    def __init__(self, db_path: str):
        """Initialize with database path."""
        self.db_path = db_path
        
    @contextmanager
    def get_db_connection(self):
        """Secure database connection context manager."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not isinstance(username, str):
            return False
        # Basic username validation - adjust as needed
        return len(username) > 3 and len(username) <= 50 and username.isalnum()
    
    def _generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def delete_account(self, username: str) -> Optional[str]:
        """
        Securely delete user account with proper validation and logging.
        
        Args:
            username: Username to delete
            
        Returns:
            Confirmation token if successful, None if error
        """
        if not self._validate_username(username):
            logger.warning(f"Invalid username format: {username}")
            return None
            
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Use parameterized query to prevent SQL injection
                query = """
                    DELETE FROM users 
                    WHERE username = ?
                    RETURNING confirmation_token
                """
                
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                
                if result:
                    confirmation_token = result['confirmation_token']
                    logger.info(f"Account deleted for user: {username}")
                    return confirmation_token
                else:
                    logger.warning(f"Account not found for user: {username}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error deleting account: {e}")
            return None