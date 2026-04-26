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
        self.lockout_time = 300  # 5 minutes in seconds

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if username in self.users:
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            return False

        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        hashed_password = self._hash_password(password, salt)

        if hashed_password == stored_hash:
            self._reset_failed_attempts(username)
            return True
        else:
            self._increment_failed_attempts(username)
            return False

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash the password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def _increment_failed_attempts(self, username: str) -> None:
        """Increment failed attempts for a user."""
        if username not in self.failed_attempts:
            self.failed_attempts[username] = 0
        self.failed_attempts[username] += 1

    def _reset_failed_attempts(self, username: str) -> None:
        """Reset failed attempts for a user."""
        if username in self.failed_attempts:
            del self.failed_attempts[username]

    def _check_lockout(self, username: str) -> bool:
        """Check if user is locked out due to too many failed attempts."""
        if username in self.failed_attempts:
            attempts = self.failed_attempts[username]
            if attempts >= self.max_attempts:
                current_time = int(time.time())
                if current_time - self.failed_attempts[username] < self.lockout_time:
                    return True
                else:
                    self._reset_failed_attempts(username)
        return False

    def log_login(self, username: str, success: bool) -> None:
        """Log successful or failed login attempts."""
        status = "successful" if success else "failed"
        logging.info(f"Login {status} for user: {username}")

# Example usage
if __name__ == "__main__":
    auth_system = AuthSystem()
    
    # Register a user
    auth_system.register("alice", "securepassword123")
    
    # Authenticate user
    success = auth_system.authenticate("alice", "securepassword123")
    auth_system.log_login("alice", success)
    
    # Attempt with wrong password
    success = auth_system.authenticate("alice", "wrongpassword")
    auth_system.log_login("alice", success)