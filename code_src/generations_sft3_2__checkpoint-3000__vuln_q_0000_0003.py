import hashlib
import secrets
import re
from typing import Dict, Tuple

class UserAuth:
    def __init__(self):
        self.users: Dict[str, Tuple[bytes, bytes]] = {}  # username: (salt, hashed_password)

    def _hash_password(self, password: str, salt: bytes) -> bytes:
        """Hash password using PBKDF2 with SHA256"""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    def _is_valid_username(self, username: str) -> bool:
        """Check if username is valid (alphanumeric, 3-20 characters)"""
        return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

    def _is_valid_password(self, password: str) -> bool:
        """Check if password is valid (at least 8 characters, 1 uppercase, 1 lowercase, 1 digit)"""
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))

    def register(self, username: str, password: str) -> bool:
        """Register a new user"""
        if not self._is_valid_username(username):
            return False
        if not self._is_valid_password(password):
            return False
        if username in self.users:
            return False
        
        salt = secrets.token_bytes(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = (salt, hashed_password)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user"""
        if username not in self.users:
            return False
        salt, stored_hash = self.users[username]
        computed_hash = self._hash_password(password, salt)
        return secrets.compare_digest(computed_hash, stored_hash)

# Example usage
auth = UserAuth()
auth.register("alice", "P@ssw0rd123")
print(auth.authenticate("alice", "P@ssw0rd123"))  # True
print(auth.authenticate("alice", "WrongPassword"))  # False