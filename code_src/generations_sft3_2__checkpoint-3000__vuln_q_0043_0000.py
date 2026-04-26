import bcrypt
import secrets
import re
from typing import Optional
import logging
from datetime import datetime
import time

class SecureUserRegistration:
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
        # Configure logging
        logging.basicConfig(filename='user_registration.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

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
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password):
            return False
        return True

    def register_user(self, email: str, password: str) -> bool:
        """Register a new user with secure password hashing"""
        try:
            # Input validation
            if not self._validate_email(email):
                logging.warning(f"Invalid email format: {email}")
                return False
            
            if not self._validate_password(password):
                logging.warning(f"Password does not meet complexity requirements: {email}")
                return False

            # Check if user already exists
            cursor = self.db.cursor()
            cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                logging.info(f"User registration attempt with existing email: {email}")
                return False

            # Generate salt and hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            # Store user with hashed password
            cursor.execute("""
                INSERT INTO users (email, password_hash, created_at)
                VALUES (%s, %s, %s)
            """, (email, hashed_password, datetime.utcnow()))
            
            self.db.commit()
            logging.info(f"New user registered: {email}")
            return True

        except Exception as e:
            # Log error without exposing sensitive details
            logging.error(f"Registration error for {email}: {type(e).__name__}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Safely retrieve user information"""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return {"id": user[0], "email": user[1]}
            return None
        except Exception as e:
            logging.error(f"Error retrieving user: {type(e).__name__}")
            return None