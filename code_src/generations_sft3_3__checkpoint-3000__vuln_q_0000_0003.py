import hashlib
import secrets
import re
from typing import Dict, Tuple

class UserAuth:
    def __init__(self):
        self.users: Dict[str, Tuple[bytes, bytes]] = {}  # username: (password_hash, salt)
        self.max_attempts = 5
        self.attempt_history: Dict[str, int] = {}

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a username and password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False  # User already exists
        
        salt = secrets.token_bytes(32)
        password_hash = self._hash_password(password, salt)
        self.users[username] = (password_hash, salt)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user with their username and password."""
        if username not in self.users:
            return False
        
        if self._check_attempts(username):
            return False  # Too many attempts
        
        password_hash = self._hash_password(password, self.users[username][1])
        if password_hash == self.users[username][0]:
            self._reset_attempts(username)
            return True
        else:
            self._increment_attempts(username)
            return False

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def _hash_password(self, password: str, salt: bytes) -> bytes:
        """Hash the password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    def _check_attempts(self, username: str) -> bool:
        """Check if the user has exceeded the maximum number of attempts."""
        attempts = self.attempt_history.get(username, 0)
        return attempts >= self.max_attempts

    def _reset_attempts(self, username: str) -> None:
        """Reset the number of attempts for a user."""
        self.attempt_history[username] = 0

    def _increment_attempts(self, username: str) -> None:
        """Increment the number of attempts for a user."""
        self.attempt_history[username] = self.attempt_history.get(username, 0) + 1

# Example usage:
auth = UserAuth()
auth.register("alice", "SecurePass123!")
is_authenticated = auth.authenticate("alice", "SecurePass123!")
print(f"Authentication successful: {is_authenticated}")