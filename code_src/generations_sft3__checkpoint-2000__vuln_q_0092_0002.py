import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Create database engine with connection pooling
        self.engine = create_engine(
            os.getenv('DATABASE_URL'),
            pool_pre_ping=True,
            pool_recycle=3600
        )

    @contextmanager
    def get_connection(self):
        """Secure connection context manager"""
        conn = None
        try:
            conn = self.engine.connect()
            yield conn
        finally:
            if conn:
                conn.close()

    def delete_user(self, user_id: int) -> bool:
        """
        Securely delete a user account from the database
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
            
        Raises:
            ValueError: If user_id is not a positive integer
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer")

        try:
            with self.get_connection() as conn:
                # Use parameterized query to prevent SQL injection
                query = text("DELETE FROM users WHERE id = :user_id")
                
                # Execute with connection
                result = conn.execute(query, {"user_id": user_id})
                
                # Check if deletion was successful
                return result.rowcount > 0

        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def __del__(self):
        """Ensure engine is properly closed"""
        if hasattr(self, 'engine'):
            self.engine.dispose()