import bcrypt
import secrets
import re
from typing import Optional

class UserAuth:
    def __init__(self):
        self.users = {}  # In a real system, use a secure database

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a username and password."""
        if not self._is_valid_username(username):
            return False
        if not self._is_strong_password(password):
            return False
        if username in self.users:
            return False
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.users[username] = hashed
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user with a username and password."""
        if not self._is_valid_username(username):
            return False
        if username not in self.users:
            return False
        hashed = self.users[username]
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def _is_valid_username(self, username: str) -> bool:
        """Check if the username is valid (alphanumeric, 3-20 characters)."""
        return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

    def _is_strong_password(self, password: str) -> bool:
        """Check if the password is strong (min 12 chars, uppercase, lowercase, digit, special char)."""
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{12,}$', password))

    def generate_reset_token(self, username: str) -> Optional[str]:
        """Generate a secure reset token for a user."""
        if username not in self.users:
            return None
        token = secrets.token_urlsafe(32)
        # In a real system, store this token securely and associate it with the user
        return token

    def verify_reset_token(self, username: str, token: str) -> bool:
        """Verify a reset token for a user."""
        # In a real system, check if the token exists and is valid for the user
        return False