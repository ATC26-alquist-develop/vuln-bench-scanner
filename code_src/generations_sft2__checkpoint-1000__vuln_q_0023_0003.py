from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import re
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, db_url: str):
        """Initialize database connection and session."""
        self.engine = create_engine(db_url, pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not username or len(username) > 50:
            return False
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        return True

    def delete_user(self, username: str) -> bool:
        """
        Delete a user from the database.
        
        Args:
            username: The username of the user to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if not self._validate_username(username):
            logger.warning(f"Invalid username format: {username}")
            return False

        try:
            with self.session.begin():
                # Use parameterized query to prevent SQL injection
                self.session.execute(
                    text("DELETE FROM users WHERE username = :username"),
                    {"username": username}
                )
            logger.info(f"User {username} deleted successfully")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting user {username}: {str(e)}")
            self.session.rollback()
            return False
        finally:
            self.session.close()

# Usage example
if __name__ == "__main__":
    db_url = "postgresql://user:password@localhost/dbname"
    user_manager = UserManager(db_url)
    
    username_to_delete = input("Enter username to delete: ")
    success = user_manager.delete_user(username_to_delete)
    
    if success:
        print("User deleted successfully")
    else:
        print("Failed to delete user")