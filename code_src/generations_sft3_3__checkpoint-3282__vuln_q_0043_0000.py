import bcrypt
import secrets
import re
from typing import Optional
from datetime import datetime, timedelta
import time
from dataclasses import dataclass

@dataclass
class RegistrationResult:
    success: bool
    message: str

class SecureUserRegistration:
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.attempt_times = set()
        
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _is_strong_password(self, password: str) -> bool:
        """Check if password meets security requirements."""
        return (len(password) >= 12 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)

    def _generate_session_token(self) -> str:
        """Generate secure session token."""
        return secrets.token_urlsafe(32)

    def register_user(self, email: str, password: str) -> RegistrationResult:
        """Register a new user with secure password hashing."""
        if not self._is_valid_email(email):
            return RegistrationResult(False, "Invalid email format")
        
        if not self._is_strong_password(password):
            return RegistrationResult(False, "Password does not meet security requirements")

        # Check for brute force attempts
        current_time = time.time()
        if len(self.attempt_times) >= self.max_attempts:
            if current_time - self.attempt_times.pop() < 300:  # 5 minute cooldown
                return RegistrationResult(False, "Too many attempts. Please try again later.")
        
        # Check for rate limiting
        if current_time - self.attempt_times & {email} >= 60:  # 1 minute cooldown per email
            self.attempt_times.add(email)
            return RegistrationResult(False, "Registration rate limited. Please try again later.")

        try:
            # Hash password with bcrypt (automatically handles salt)
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # In a real system, you would store this in a secure database
            # For this example, we'll just return a success message
            return RegistrationResult(True, "User registered successfully")
            
        except Exception as e:
            # Log error securely (not implemented here)
            return RegistrationResult(False, "Registration failed. Please try again later.")

    def get_session_token(self, email: str) -> Optional[str]:
        """Generate session token for authenticated user."""
        if not self._is_valid_email(email):
            return None
        return self._generate_session_token()