import bcrypt
import secrets
import re
from typing import Optional

class UserAuth:
    def __init__(self):
        self.users = {}  # In a real system, use a secure database instead

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if not self._is_valid_username(username) or not self._is_strong_password(password):
            return False
        if username in self.users:
            return False
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = hashed
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user with secure password verification."""
        if not self._is_valid_username(username):
            return False
        stored_hash = self.users.get(username)
        if stored_hash is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    def _is_valid_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _is_strong_password(self, password: str) -> bool:
        """Check if password meets security requirements."""
        return (len(password) >= 12 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user's password after verifying old password."""
        if not self.authenticate_user(username, old_password):
            return False
        if not self._is_strong_password(new_password):
            return False
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = hashed
        return True

    def generate_reset_token(self, username: str) -> Optional[str]:
        """Generate a secure reset token for password reset."""
        if not self.authenticate_user(username, secrets.token_urlsafe(32)):
            return None
        token = secrets.token_urlsafe(32)
        # In a real system, store this token securely and associate it with the user
        return token