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
        self.db_connection = db_connection
        # Configure secure logging
        logging.basicConfig(filename='user_registration.log', 
                          level=logging.INFO,
                          format='%(asctime)s - %(levelname)s - %(message)s')
        
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 12:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
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

            # Check for existing user
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                logging.info(f"Registration attempt with existing email: {email}")
                return None

            # Generate salt and hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Store user with hashed password
            cursor.execute("""
                INSERT INTO users (email, password_hash, created_at)
                VALUES (%s, %s, %s)
            """, (email, hashed_password, datetime.utcnow()))
            
            self.db_connection.commit()
            
            logging.info(f"New user registered: {email}")
            return True

        except Exception as e:
            # Log error without exposing sensitive details
            logging.error(f"Registration error: {str(e)}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def verify_user(self, email: str, password: str) -> bool:
        """Verify user credentials"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT 1 FROM users 
                WHERE email = %s AND password_hash = %s
            """, (email, password.encode('utf-8')))
            result = cursor.fetchone()
            return bool(result)
        except Exception:
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()