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
    password_hash: str
    salt: bytes
    created_at: datetime

class LoginStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    RATE_LIMITED = "rate_limited"

class SecureLoginSystem:
    def __init__(self):
        self.users = {}  # In production, use secure database
        self.login_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        self.ph = PasswordHasher()
        self._reset_attempts()

    def _reset_attempts(self):
        """Reset login attempts after lockout period"""
        for username in list(self.login_attempts.keys()):
            if datetime.now() - self.login_attempts[username] > self.lockout_duration:
                del self.login_attempts[username]

    def _is_rate_limited(self, username: str) -> bool:
        """Check if user is rate limited"""
        return username in self.login_attempts and \
               self.login_attempts[username] and \
               datetime.now() - self.login_attempts[username] < self.lockout_duration

    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing"""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        if username in self.users:
            return False

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        self.users[username] = User(
            username=username,
            password_hash=password_hash.decode(),
            salt=salt,
            created_at=datetime.utcnow()
        )
        return True

    def login(self, username: str, password: str) -> tuple[LoginStatus, Optional[str]]:
        """Perform secure login"""
        if not self._validate_username(username) or not self._validate_password(password):
            return LoginStatus.INVALID_CREDENTIALS, None

        if self._is_rate_limited(username):
            return LoginStatus.RATE_LIMITED, None

        if username not in self.users:
            return LoginStatus.INVALID_CREDENTIALS, None

        try:
            self.ph.verify(self.users[username].password_hash, password)
            self._reset_attempts()
            return LoginStatus.SUCCESS, username
        except VerifyMismatchError:
            self.login_attempts[username] = datetime.now()
            return LoginStatus.INVALID_CREDENTIALS, None
        except Exception:
            return LoginStatus.INVALID_CREDENTIALS, None

    def logout(self, username: str) -> None:
        """Simulate logout"""
        # In production, implement proper session management
        pass