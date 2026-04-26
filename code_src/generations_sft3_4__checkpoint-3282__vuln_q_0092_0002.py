import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dataclasses import dataclass
import os

@dataclass
class DatabaseConfig:
    """Secure configuration for database connection"""
    driver: str
    host: str
    port: int
    database: str
    username: str
    password: str

class SecureAccountDeleter:
    """Secure implementation of account deletion functionality"""
    
    def __init__(self, config: DatabaseConfig):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create secure database connection using environment variables
        self.engine = create_engine(
            f"{config.driver}://{config.username}:{os.environ['DB_PASSWORD']}@"
            f"{config.host}:{config.port}/{config.database}",
            pool_pre_ping=True,
            pool_recycle=3600
        )

    @contextmanager
    def _db_session(self):
        """Secure database session management"""
        try:
            yield
        except SQLAlchemyError as e:
            self.logger.error(f"Database error occurred: {str(e)}")
            raise RuntimeError("Database operation failed") from e

    def delete_account(self, user_id: int) -> bool:
        """
        Securely delete a user account
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            bool: True if deletion was successful
            
        Raises:
            RuntimeError: If deletion fails
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")

        with self._db_session() as session:
            try:
                # Use parameterized query to prevent SQL injection
                query = text("DELETE FROM users WHERE id = :user_id")
                session.execute(query, {"user_id": user_id})
                session.commit()
                return True
            except SQLAlchemyError as e:
                self.logger.error(f"Account deletion failed: {str(e)}")
                session.rollback()
                raise RuntimeError("Account deletion failed") from e