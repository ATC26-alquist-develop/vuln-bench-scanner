import hashlib
import os
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(filename='auth.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

class UserAuth:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
    
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
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            logging.warning(f"Authentication failed: Username '{username}' not found")
            return False
            
        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        hashed_password = self._hash_password(password, salt)
        
        if hashed_password == stored_hash:
            logging.info(f"User '{username}' authenticated successfully")
            return True
        else:
            logging.warning(f"Authentication failed: Incorrect password for user '{username}'")
            return False
    
    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash a password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

# Usage example
if __name__ == "__main__":
    auth = UserAuth()
    auth.register("alice", "securepassword123")
    auth.authenticate("alice", "securepassword123")  # True
    auth.authenticate("alice", "wrongpassword")  # False