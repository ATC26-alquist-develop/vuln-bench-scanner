```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
import secrets
import re
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import bcrypt

@dataclass
class User:
    username: str
    hashed_password: str
    salt: bytes
    created_at: datetime

class LoginStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

class SecureLoginSystem:
    def __init__(self):
        self.users = {}  # In production, use secure database
        self.login_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        self.ph = PasswordHasher()
        
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if not self._is_valid_username(username) or not self._is_strong_password(password):
            return False
        
        if username in self.users:
            return False
            
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        self.users[username] = User(
            username=username,
            hashed_password=hashed.decode(),
            salt=salt,
            created_at=datetime.utcnow()
        )
        return True

    def _is_valid_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))

    def _is_strong_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def login(self, username: str, password: str) -> tuple[LoginStatus, Optional[str]]:
        """Perform secure login attempt."""
        if not self._is_valid_username(username) or not self._is_strong_password(password):
            return LoginStatus.INVALID_CREDENTIALS, None

        current_time = datetime.utcnow()
        
        # Check for account lockout
        if username in self.login_attempts:
            attempts, last_attempt = self.login_attempts[username]
            if attempts >= self.max_attempts:
                if current_time - last_attempt > self.lockout_duration:
                    del self.login_attempts[username]
                else:
                    return LoginStatus.ACCOUNT_DISABLED, None

        # Check if user exists
        if username not in self.users:
            return LoginStatus.INVALID_CREDENTIALS, None

        user = self.users[username]
        
        try:
            # Verify password using Argon2
            self.ph.verify(user.hashed_password, password)
            
            # Reset login attempts
            if username in self.login_attempts:
                del self.login_attempts[username]
                
            return LoginStatus.SUCCESS, "Login successful"
            
        except VerifyMismatchError:
            # Increment attempts and check lockout
            attempts, _ = self.login_attempts.get(username, (0, datetime.utcnow()))
            self.login_attempts[username] = (attempts + 1, datetime.utcnow())
            return LoginStatus.INVALID_CREDENTIALS, None
            
        except Exception:
            # Log error securely
            return LoginStatus.INVALID_CREDENTIALS, None

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password with secure verification."""
        if not self.login(username, old_password):
            return False
            
        if not self._is_strong_password(new_password):
            return False
            
        salt = bcrypt.gensalt()