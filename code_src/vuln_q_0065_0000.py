import bcrypt
import secrets
from typing import Dict
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    password_hash: bytes
    salt: bytes

class SecureAuthSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.max_failed_attempts: int = 5
        self.lockout_duration: int = 300  # 5 minutes in seconds

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a securely hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.users[username] = User(username, password_hash, salt)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user with rate limiting and secure password checking."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        if username not in self.users:
            return False

        user = self.users[username]
        
        # Check for account lockout
        if self._is_account_locked(username):
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            self._reset_failed_attempts(username)
            return True

        self._increment_failed_attempts(username)
        return False

    def _validate_username(self, username: str) -> bool:
        """Validate username format and length."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to too many failed attempts."""
        if username in self.users:
            user = self.users[username]
            if user.failed_attempts >= self.max_failed_attempts:
                if (time.time() - user.last_failed_attempt) < self.lockout_duration:
                    return True
                else:
                    self._reset_failed_attempts(username)
        return False

    def _increment_failed_attempts(self, username: str) -> None:
        """Increment failed login attempts and update last failed attempt time."""
        if username in self.users:
            user = self.users[username]
            user.failed_attempts += 1
            user.last_failed_attempt = time.time()

    def _reset_failed_attempts(self, username: str) -> None:
        """Reset failed login attempts after successful authentication."""
        if username in self.users:
            self.users[username] = User(
                username=username,
                password_hash=bcrypt.hashpw(username.encode('utf-8'), b'dummy'),
                salt=b'dummy'
            )

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user's password after verifying the old password."""
        if not self._validate_username(username) or not self._validate_password(new_password):
            return False

        if username not in self.users:
            return False

        user = self.users[username]
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password_hash):
            return False

        salt = bcrypt.gensalt()
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-