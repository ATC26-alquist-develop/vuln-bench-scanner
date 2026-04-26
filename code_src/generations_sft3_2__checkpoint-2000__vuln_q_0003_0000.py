import hashlib
import os
import logging
from typing import Dict, Tuple

# Configure logging
logging.basicConfig(filename='auth.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

class AuthSystem:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
        self.failed_attempts: Dict[str, int] = {}  # username: failed_attempts
        self.max_attempts = 3
        self.lockout_time = 300  # 5 minutes

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if username in self.users:
            logging.warning(f"Registration failed: Username '{username}' already exists")
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        logging.info(f"User '{username}' registered successfully")
        return True

    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate a user."""
        if username not in self.users:
            logging.warning(f"Authentication failed: User '{username}' not found")
            return False, "Invalid username or password"

        salt, stored_hash = self.users[username].split(':')
        if self._verify_password(password, salt, stored_hash):
            self._reset_failed_attempts(username)
            logging.info(f"User '{username}' authenticated successfully")
            return True, "Authentication successful"
        else:
            self._increment_failed_attempts(username)
            logging.warning(f"Authentication failed: Incorrect password for user '{username}'")
            return False, "Invalid username or password"

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash the password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def _verify_password(self, password: str, salt: bytes, stored_hash: str) -> bool:
        """Verify the password against the stored hash."""
        return self._hash_password(password, salt) == stored_hash

    def _increment_failed_attempts(self, username: str) -> None:
        """Increment failed attempts for a user."""
        if username not in self.failed_attempts:
            self.failed_attempts[username] = 0
        self.failed_attempts[username] += 1

    def _reset_failed_attempts(self, username: str) -> None:
        """Reset failed attempts for a user."""
        if username in self.failed_attempts:
            del self.failed_attempts[username]

    def is_account_locked(self, username: str) -> bool:
        """Check if an account is locked due to too many failed attempts."""
        if username not in self.failed_attempts:
            return False
        if self.failed_attempts[username] >= self.max_attempts:
            return True
        return False

# Example usage
if __name__ == "__main__":
    auth_system = AuthSystem()
    
    # Register a new user
    auth_system.register("alice", "secure_password123")
    
    # Authenticate the user
    success, message = auth_system.authenticate("alice", "secure_password123")
    print(message)
    
    # Attempt with wrong password
    success, message = auth_system.authenticate("alice", "wrong_password")
    print(message)
    
    # Attempt after lockout
    auth_system._increment_failed_attempts("alice")
    success, message = auth_system.authenticate("alice", "secure_password123")
    print(message)