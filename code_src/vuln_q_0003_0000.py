import logging
import hashlib
import os
import re
from typing import Optional

# Configure logging
logging.basicConfig(
    filename='auth.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class UserAuth:
    def __init__(self):
        self.users = {}  # In a real system, use a secure database
        self.failed_attempts = {}

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = {'hash': hashed_password, 'salt': salt}
        return True

    def login(self, username: str, password: str) -> bool:
        """Authenticate a user and log successful login."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        if username not in self.users:
            return False

        user = self.users[username]
        hashed_password = self._hash_password(password, user['salt'])

        if hashed_password == user['hash']:
            self._log_successful_login(username)
            return True

        self._increment_failed_attempts(username)
        return False

    def _hash_password(self, password: str, salt: bytes) -> bytes:
        """Hash a password with a salt using SHA-256."""
        return hashlib.pbkdf2_hmac(
            'sha256', password.encode(), salt, 100000
        )

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 8 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def _increment_failed_attempts(self, username: str) -> None:
        """Increment failed login attempts."""
        self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1

    def _log_successful_login(self, username: str) -> None:
        """Log a successful login attempt."""
        logging.info(f"Successful login: {username}")

# Example usage
if __name__ == "__main__":
    auth = UserAuth()
    
    # Register a user
    username = "john_doe"
    password = "SecurePass123"
    if auth.register(username, password):
        print(f"User {username} registered successfully")
    else:
        print(f"Failed to register user {username}")

    # Attempt to login
    if auth.login(username, password):
        print(f"User {username} logged in successfully")
    else:
        print(f"Failed login attempt for user {username}")