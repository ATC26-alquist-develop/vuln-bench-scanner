import bcrypt
import secrets
import re
from typing import Optional
import logging
from datetime import datetime
import json
from pathlib import Path

class SecureUserRegistration:
    def __init__(self, data_file: str = "users.json"):
        """Initialize with secure defaults."""
        self.data_file = Path(data_file)
        self.users = self._load_users()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up secure logging configuration."""
        logger = logging.getLogger("SecureUserRegistration")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("registration.log", mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _load_users(self) -> dict:
        """Securely load user data from file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                self.logger.error("Invalid JSON in data file")
                return {}
        return {}
    
    def _save_users(self) -> None:
        """Securely save user data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.users, f)
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _is_strong_password(self, password: str) -> bool:
        """Check if password meets security requirements."""
        return (len(password) >= 12 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)
    
    def register_user(self, email: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        try:
            # Input validation
            if not email or not password:
                self.logger.warning("Empty email or password attempt")
                return False
                
            if not self._is_valid_email(email):
                self.logger.warning(f"Invalid email format: {email}")
                return False
                
            if not self._is_strong_password(password):
                self.logger.warning("Weak password attempt")
                return False
            
            # Check if user already exists
            if email in self.users:
                self.logger.warning(f"Attempt to register existing email: {email}")
                return False
                
            # Generate salt and hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Store user with hashed password
            self.users[email] = {
                'password': hashed.decode('utf-8'),
                'created_at': datetime.utcnow().isoformat()
            }
            self._save_users()
            
            self.logger.info(f"New user registered: {email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Registration error: {str(e)}")
            return False