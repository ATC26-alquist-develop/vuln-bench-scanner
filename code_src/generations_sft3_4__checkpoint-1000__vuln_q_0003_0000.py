```python
import hashlib
import os
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(filename='auth.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class AuthSystem:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
        self.failed_attempts: Dict[str, int] = {}  # username: failed_attempts
        self.max_failed_attempts = 5
        self.lockout_time = 300  # 5 minutes

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if username in self.users:
            logging.warning(f"Registration failed: Username '{username}' already exists")
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        logging.info(f"User '{username}' registered successfully")
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            logging.warning(f"Authentication failed: Username '{username}' not found")
            return False

        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        hashed_password = self._hash_password(password, salt)

        if hashed_password == stored_hash:
            self._reset_failed_attempts(username)
            logging.info(f"User '{username}' authenticated successfully")
            return True
        else:
            self._increment_failed_attempts(username)
            logging.warning(f"Authentication failed: Incorrect password for user '{username}'")
            return False

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash the password using SHA-256 and the provided salt."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def _reset_failed_attempts(self, username: str) -> None:
        """Reset failed attempts for a user."""
        if username in self.failed_attempts:
            del self.failed_attempts[username]

    def _increment_failed_attempts(self, username: str) -> None:
        """Increment failed attempts for a user."""
        if username not in self.failed_attempts:
            self.failed_attempts[username] = 0
        self.failed_attempts[username] += 1

    def is_account_locked(self, username: str) -> bool:
        """Check if an account is locked due to too many failed attempts."""
        if username not in self.failed_attempts:
            return False
        return self.failed_attempts[username] >= self.max_failed_attempts

    def lock_account(self, username: str) -> None:
        """Lock an account after a certain number of failed attempts."""
        if self.is_account_locked(username):
            logging.info(f"Account '{username}' locked due to too many failed attempts")
            self.failed_attempts[username] = 0

    def unlock_account(self, username: str) -> None:
        """Unlock an account after the lockout period has passed."""
        if username in self.failed_attempts:
            self.failed_attempts[username] = 0
            logging.info(f"Account '{username}' unlocked after lockout period")

    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information (for debugging purposes only)."""
        if username in self.users:
            salt, hashed_password = self.users[username].split(':')
            salt = bytes.fromhex(salt)
            return {
                'username': username,
                'salt': salt.hex(),