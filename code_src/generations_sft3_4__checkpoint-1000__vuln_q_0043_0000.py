import bcrypt
import secrets
import re
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class UserRegistrationResult:
    success: bool
    message: str
    user_id: Optional[str] = None

class SecureUserRegistration:
    def __init__(self, max_password_length: int = 128):
        self.max_password_length = max_password_length
        self.users = {}  # In-memory storage - for demonstration purposes only

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
                return UserRegistrationResult(False, "Invalid email format")
            
            if not self._validate_password(password):
                return UserRegistrationResult(False, "Password does not meet security requirements")

            # Generate a cryptographically secure random salt
            salt = bcrypt.gensalt()

            # Hash the password with the salt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            # Generate a secure user ID
            user_id = secrets.token_hex(16)

            # Store user data (in a real system, use a secure database)
            self.users[user_id] = {
                'email': email,
                'password_hash': hashed_password,
                'created_at': datetime.utcnow(),
                'last_login': None
            }

            return UserRegistrationResult(True, "User registered successfully", user_id)

        except Exception as e:
            # Log the error securely (implement proper logging)
            return UserRegistrationResult(False, "Registration failed")

    def verify_user(self, user_id: str) -> bool:
        """Verify if a user exists."""
        return user_id in self.users