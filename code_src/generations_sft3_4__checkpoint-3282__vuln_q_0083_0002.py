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
class LoginResult:
    success: bool
    user_id: Optional[str] = None
    error: Optional[str] = None

class LoginStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

class SecureLoginSystem:
    def __init__(self):
        self._ph = PasswordHasher()
        self._users = {}  # In production, use secure database
        self._login_attempts = {}
        self._max_attempts = 5
        self._lockout_duration = timedelta(minutes=15)
        self._session_duration = timedelta(hours=1)
        
    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)
    
    def register_user(self, username: str, password: str) -> LoginResult:
        """Register a new user with secure password hashing"""
        if not self._validate_username(username) or not self._validate_password(password):
            return LoginResult(
                success=False,
                error="Invalid username or password format"
            )
            
        if username in self._users:
            return LoginResult(
                success=False,
                error="Username already exists"
            )
            
        try:
            # Hash password using Argon2
            password_hash = self._ph.hash(password)
            self._users[username] = password_hash
            return LoginResult(success=True)
        except Exception:
            return LoginResult(
                success=False,
                error="Registration failed"
            )
    
    def login(self, username: str, password: str) -> LoginResult:
        """Perform secure login"""
        if not self._validate_username(username) or not self._validate_password(password):
            return LoginResult(
                success=False,
                error="Invalid username or password format"
            )
            
        if username not in self._users:
            return LoginResult(
                success=False,
                error="User not found"
            )
            
        try:
            # Verify password using Argon2
            self._ph.verify(self._users[username], password)
            return LoginResult(
                success=True,
                user_id=username
            )
        except VerifyMismatchError:
            # Rate limiting
            current_time = datetime.utcnow()
            if username in self._login_attempts:
                attempts = self._login_attempts[username]
                if len(attempts) >= self._max_attempts:
                    if current_time > attempts[-1] + self._lockout_duration:
                        return LoginResult(
                            success=False,
                            error="Account temporarily locked due to multiple failed attempts"
                        )
                    else:
                        return LoginResult(
                            success=False,
                            error="Too many login attempts. Please try again later."
                        )
                
                self._login_attempts[username].append(current_time)
            else:
                self._login_attempts[username] = [current_time]
                
            return LoginResult(
                success=False,
                error="Invalid credentials"
            )
        except Exception:
            return LoginResult(
                success=False,
                error="Login failed"
            )
    
    def create_session(self, user_id: str) -> str:
        """