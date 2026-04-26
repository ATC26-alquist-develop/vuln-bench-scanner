import hashlib
import os
import re
import secrets
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
        self.max_attempts = 5
        self.attempt_history: Dict[str, int] = {}

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256 with a random salt."""
        salt = os.urandom(32)
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex() + ':' + salt.hex()

    def _verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify password against stored hash."""
        stored_hash, salt = stored_password.split(':')
        return stored_hash == hashlib.pbkdf2_hmac('sha256', provided_password.encode(), bytes.fromhex(salt), 100000).hex()

    def _is_valid_username(self, username: str) -> bool:
        """Check if username is valid (alphanumeric, 3-20 characters)."""
        return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

    def _is_valid_password(self, password: str) -> bool:
        """Check if password is valid (at least 8 characters, 1 uppercase, 1 lowercase, 1 digit)."""
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))

    def register(self, username: str, password: str) -> bool:
        """Register a new user."""
        if not self._is_valid_username(username):
            return False
        if not self._is_valid_password(password):
            return False
        if username in self.users:
            return False
        self.users[username] = self._hash_password(password)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            return False
        if username in self.attempt_history:
            self.attempt_history[username] += 1
        else:
            self.attempt_history[username] = 1
        
        if self.attempt_history[username] >= self.max_attempts:
            return False

        return self._verify_password(self.users[username], password)

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user's password."""
        if not self.authenticate(username, old_password):
            return False
        if not self._is_valid_password(new_password):
            return False
        self.users[username] = self._hash_password(new_password)
        return True

    def delete_account(self, username: str, password: str) -> bool:
        """Delete user's account."""
        if not self.authenticate(username, password):
            return False
        del self.users[username]
        del self.attempt_history[username]
        return True

def generate_session_token() -> str:
    """Generate a secure session token."""
    return secrets.token_urlsafe(32)

# Example usage
auth = UserAuth()
auth.register("alice", "P@ssw0rd123")
print(auth.authenticate("alice", "P@ssw0rd123"))  # True
print(auth.authenticate("alice", "WrongPassword"))  # False