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
    engine = None
    
    @classmethod
    def init(cls):
        """Initialize database connection securely"""
        # Use environment variables for sensitive data
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise ValueError("Database URL not configured")
            
        cls.engine = create_engine(db_url, pool_pre_ping=True)
        
    @contextmanager
    def get_session(self):
        """Secure session management"""
        session = self.engine.connect()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

def delete_user_account(user_id: int) -> bool:
    """
    Securely delete a user account from the database
    
    Args:
        user_id: ID of the user to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
        
    Raises:
        ValueError: If user_id is invalid
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")

    try:
        with DatabaseConfig.get_session() as session:
            # Use parameterized query to prevent SQL injection
            query = text("DELETE FROM users WHERE id = :user_id")
            
            result = session.execute(query, {"user_id": user_id})
            
            # Check if any rows were affected
            return result.rowcount > 0
            
    except SQLAlchemyError as e:
        logging.error(f"Database error during user deletion: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during user deletion: {str(e)}")
        return False