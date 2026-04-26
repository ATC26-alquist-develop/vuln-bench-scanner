import secrets
import hashlib
import re
from typing import Tuple
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class SecureUserRegistration:
    def __init__(self, min_length: int = 12, max_length: int = 64):
        self.min_length = min_length
        self.max_length = max_length
        self.ph = PasswordHasher()
        
    def _validate_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        if len(password) < self.min_length:
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

    def register_user(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user with secure password hashing.
        Returns: Tuple of (success: bool, message: str)
        """
        try:
            # Validate inputs
            if not isinstance(email, str) or not isinstance(password, str):
                return False, "Invalid input types"
            
            if not self._validate_email(email):
                return False, "Invalid email format"
            
            if not self._validate_password(password):
                return False, "Password does not meet security requirements"

            # Generate secure salt
            salt = secrets.token_bytes(16)
            
            # Hash password with Argon2
            hashed_password = self.ph.hash(password + salt.hex())
            
            # Store hashed password and salt (in real system, use secure database)
            # This is a simplified example, in practice use a secure database
            
            return True, "User registered successfully"
            
        except Exception as e:
            # Log error securely here
            return False, "Registration failed"