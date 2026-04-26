import hashlib
import os
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(filename='auth.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

class AuthSystem:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
        self.failed_attempts: Dict[str, int] = {}  # username: failed_attempts
        self.max_failed_attempts = 5
        self.lockout_duration = 300  # 5 minutes in seconds

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if username in self.users:
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        logging.info(f"User registered: {username}")
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            logging.warning(f"Authentication attempt for non-existent user: {username}")
            return False

        current_time = int(time.time())
        
        # Check for lockout
        if username in self.failed_attempts and \
           self.failed_attempts[username] >= self.max_failed_attempts:
            if current_time - self.failed_attempts[username] < self.lockout_duration:
                logging.warning(f"Account locked due to too many failed attempts: {username}")
                return False

        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        
        # Hash the provided password with the stored salt
        hashed_password = self._hash_password(password, salt)
        
        # Compare hashes
        if hashed_password == stored_hash:
            logging.info(f"Successful login: {username}")
            self.failed_attempts.pop(username, None)
            return True
        else:
            logging.warning(f"Failed login attempt: {username}")
            self.failed_attempts[username] = current_time
            return False

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> str:
        """Hash the password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

# Example usage
if __name__ == "__main__":
    auth_system = AuthSystem()
    
    # Register users
    auth_system.register_user("alice", "password123")
    auth_system.register_user("bob", "securepass")
    
    # Authenticate users
    print(auth_system.authenticate("alice", "password123"))  # True
    print(auth_system.authenticate("bob", "wrongpass"))  # False
    print(auth_system.authenticate("eve", "hackpass"))  # False