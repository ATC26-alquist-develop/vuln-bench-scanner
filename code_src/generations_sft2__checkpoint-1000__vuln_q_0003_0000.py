import logging
from typing import Optional
from datetime import datetime
import bcrypt
import secrets
import re

class UserAuth:
    def __init__(self):
        # Configure logging
        logging.basicConfig(filename='auth.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Simulated database of users (in a real system, use a proper database)
        self.users = {}
        
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a secure password."""
        if not self._is_valid_username(username):
            logging.warning(f"Invalid username attempt: {username}")
            return False
            
        if not self._is_strong_password(password):
            logging.warning(f"Weak password attempt: {username}")
            return False
            
        if username in self.users:
            logging.warning(f"Username already exists: {username}")
            return False
            
        # Hash password with salt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Store user (in a real system, use a proper database)
        self.users[username] = hashed_password
        logging.info(f"New user registered: {username}")
        return True
        
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            logging.warning(f"Login attempt with non-existent username: {username}")
            return False
            
        stored_hash = self.users[username]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            logging.info(f"Successful login: {username}")
            return True
        else:
            logging.warning(f"Failed login attempt: {username}")
            return False
            
    def _is_valid_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))
        
    def _is_strong_password(self, password: str) -> bool:
        """Check if password meets strength requirements."""
        return (len(password) >= 12 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)