```python
import bcrypt
import secrets
import re
from typing import Optional
import logging
from datetime import datetime, timedelta

class SecureUserRegistration:
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db_connection = db_connection
        # Configure secure logging
        logging.basicConfig(
            filename='user_registration.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 12:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            return False
        return True

    def register_user(self, email: str, password: str) -> Optional[bool]:
        """Register a new user with secure password hashing"""
        try:
            # Input validation
            if not self._validate_email(email):
                logging.warning(f"Invalid email format: {email}")
                return None
                
            if not self._validate_password(password):
                logging.warning(f"Password does not meet complexity requirements: {email}")
                return None

            # Generate salt and hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            # Generate secure token for account verification
            verification_token = secrets.token_urlsafe(32)

            # Store user with hashed password and verification token
            query = """
                INSERT INTO users (email, password_hash, password_salt, 
                                 verification_token, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor = self.db_connection.cursor()
            cursor.execute(query, (email, hashed_password, salt, verification_token, datetime.utcnow()))
            self.db_connection.commit()

            # Log successful registration
            logging.info(f"User registered successfully: {email}")
            return True

        except Exception as e:
            # Log error without exposing sensitive information
            logging.error(f"Registration failed for {email}: {type(e).__name__}")
            self.db_connection.rollback()
            return None

    def verify_account(self, email: str, token: str) -> bool:
        """Verify user account with secure token comparison"""
        try:
            query = """
                SELECT password_hash, verification_token, created_at 
                FROM users 
                WHERE email = %s
            """
            cursor = self.db_connection.cursor()
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if not result:
                return False

            stored_hash, stored_token, created_at = result
            if not secrets.compare_digest(stored_token, token):
                return False

            # Verify token hasn't expired (1 hour)
            if datetime.utcnow() - created_at > timedelta(hours=1):
                return False

            # Generate new token for future password changes
            new_token = secrets.token_urlsafe(32)
            query = """
                UPDATE users 
                SET verification_token = %s 
                WHERE email = %s
            """
            cursor.execute(query, (new_token, email))
            self.db_connection.commit()

            return True

        except Exception as e:
            logging