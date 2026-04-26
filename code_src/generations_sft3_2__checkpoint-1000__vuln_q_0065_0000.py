import bcrypt
import secrets
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users: Dict[str, bytes] = {}

    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user with a hashed password.
        """
        if username in self.users:
            return False  # User already exists
        
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Store the hashed password
        self.users[username] = hashed_password
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate a user by comparing the provided password with the stored hash.
        """
        if username not in self.users:
            return False  # User not found
        
        stored_hash = self.users[username]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    def generate_session_token(self) -> str:
        """
        Generate a secure session token for authenticated users.
        """
        return secrets.token_urlsafe(32)

# Example usage
auth = UserAuth()

# Register a new user
auth.register_user("alice", "secure_password123")

# Authenticate user
is_authenticated = auth.authenticate_user("alice", "secure_password123")
print(f"Authentication result: {is_authenticated}")

# Generate session token
session_token = auth.generate_session_token()
print(f"Session token: {session_token}")