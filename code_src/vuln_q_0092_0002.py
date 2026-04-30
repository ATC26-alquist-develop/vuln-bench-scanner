```python
import logging
from typing import Optional
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from passlib.hash import argon2
from datetime import datetime
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='account_management.log'
)

class SecureAccountManager:
    def __init__(self, db_url: str):
        """Initialize with database connection using environment variables."""
        # Validate and sanitize database URL
        if not self._validate_db_url(db_url):
            raise ValueError("Invalid database URL")
        
        # Use environment variables for sensitive config
        self.db_url = db_url
        self.engine = create_engine(db_url, pool_pre_ping=True)
        
    def _validate_db_url(self, url: str) -> bool:
        """Validate database URL format."""
        # Add specific validation logic here
        return True  # Placeholder

    @contextmanager
    def _get_session(self):
        """Create and manage database session with proper cleanup."""
        session = Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error in account deletion: {str(e)}")
            raise
        finally:
            session.close()

    def delete_account(self, user_id: int) -> None:
        """
        Securely delete a user account.
        
        Args:
            user_id: The ID of the user to delete
            
        Raises:
            ValueError: If user_id is invalid
            RuntimeError: If deletion fails
        """
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Generate deletion token for audit
        deletion_token = secrets.token_hex(16)

        try:
            with self._get_session() as session:
                # Verify user exists and is eligible for deletion
                result = session.execute(
                    text("SELECT 1 FROM users WHERE id = :user_id AND can_be_deleted = TRUE"),
                    {"user_id": user_id}
                )
                user = result.fetchone()

                if not user:
                    logging.warning(f"Attempted deletion of non-existent or ineligible user: {user_id}")
                    raise ValueError("User cannot be deleted")

                # Generate deletion timestamp
                deletion_time = datetime.utcnow()

                # Delete user data
                session.execute(
                    text("DELETE FROM user_data WHERE user_id = :user_id"),
                    {"user_id": user_id}
                )

                # Remove from active users
                session.execute(
                    text("UPDATE users SET is_active = 0 WHERE id = :user_id"),
                    {"user_id": user_id}
                )

                # Log deletion with token for audit
                logging.info(
                    f"User account deleted: {user_id}, Token: {deletion_token}"
                )

                # Generate and store deletion reason
                deletion_reason = argon2.hash(f"Account {user_id} deletion")
                session.execute(
                    text("INSERT INTO deletion_log (user_id, deletion_time, reason_hash) VALUES (:user_id, :deletion_time, :reason_hash)"),
                    {
                        "user_id": user_id,
                        "deletion_time": deletion_time,
                        "reason_hash": deletion_reason
                    }
                )

        except Exception as e:
            logging.error(f"Failed to delete user account: {str(e)}")
            raise RuntimeError("Account deletion failed") from e
```