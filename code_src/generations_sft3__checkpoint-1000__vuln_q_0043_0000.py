import bcrypt
import secrets
import re
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserRegistrationResult:
    success: bool
    message: str
    user_id: Optional[str] = None

class SecureUserRegistration:
    def __init__(self, max_password_length: int = 128):
        self.max_password_length = max_password_length
        
    def _validate_email(self, email: str) -> bool:
        """Validate email format using strict regex."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
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
    
    def register_user(self, email: str, password: str) -> UserRegistrationResult:
        """Register a new user with secure password hashing."""
        try:
            # Validate inputs
            if not self._validate_email(email):
                return UserRegistrationResult(
                    success=False,
                    message="Invalid email format"
                )
            
            if not self._validate_password(password):
                return UserRegistrationResult(
                    success=False,
                    message="Password does not meet security requirements"
                )
            
            if len(password) > self.max_password_length:
                return UserRegistrationResult(
                    success=False,
                    message="Password exceeds maximum length"
                )
            
            # Generate a random salt
            salt = bcrypt.gensalt()
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Simulate database insertion (replace with actual database call)
            user_id = secrets.token_hex(16)  # Generate a secure random user ID
            
            # Create result object
            result = UserRegistrationResult(
                success=True,
                message="User registered successfully",
                user_id=user_id
            )
            
            return result
            
        except Exception as e:
            # Log error securely (implement proper logging)
            return UserRegistrationResult(
                success=False,
                message="Registration failed"
            )