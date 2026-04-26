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
            return False  # User already exists
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        self.failed_attempts[username] = 0
        logging.info(f"User registered: {username}")
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            logging.warning(f"Authentication attempt for non-existent user: {username}")
            return False

        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        hashed_password = self._hash_password(password, salt)

        if hashed_password == stored_hash:
            self.failed_attempts[username] = 0
            logging.info(f"Successful login: {username}")
            return True
        else:
            self.failed_attempts[username] += 1
            logging.warning(f"Failed login attempt: {username}")
            return False

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash the password using SHA-256 with the given salt."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def is_account_locked(self, username: str) -> bool:
        """Check if the user's account is locked due to too many failed attempts."""
        if username not in self.failed_attempts:
            return False
        
        current_time = int(time.time())
        if self.failed_attempts[username] >= self.max_failed_attempts:
            if current_time - self.failed_attempts[username] > self.lockout_time:
                self.failed_attempts[username] = 0
                return False
            return True
        return False

    def reset_failed_attempts(self, username: str) -> None:
        """Reset failed login attempts for a user."""
        if username in self.failed_attempts:
            self.failed_attempts[username] = 0
            logging.info(f"Failed attempts reset for user: {username}")