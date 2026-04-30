```python
import hashlib
import os
import re
import secrets
from typing import Tuple

class UserAuth:
    def __init__(self):
        self.users = {}  # In real-world, use a secure database
        self.sessions = {}

    def register(self, username: str, password: str) -> bool:
        """Register a new user with username and password."""
        if not self._validate_username(username):
            raise ValueError("Invalid username format")
        
        if not self._validate_password(password):
            raise ValueError("Password does not meet security requirements")
        
        if username in self.users:
            raise ValueError("Username already exists")
        
        salt = secrets.token_bytes(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = {
            'password': hashed_password,
            'salt': salt
        }
        return True

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate a user and return session token if successful."""
        if username not in self.users:
            return False, ""
        
        user = self.users[username]
        hashed_password = self._hash_password(password, user['salt'])
        
        if hashed_password == user['password']:
            session_token = secrets.token_urlsafe(32)
            self.sessions[session_token] = username
            return True, session_token
        return False, ""

    def logout(self, session_token: str) -> None:
        """Invalidate a user session."""
        if session_token in self.sessions:
            del self.sessions[session_token]

    def _hash_password(self, password: str, salt: bytes) -> bytes:
        """Hash a password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt, 
            100000  # Number of iterations
        )

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return (
            len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        )

# Example usage
if __name__ == "__main__":
    auth = UserAuth()
    
    try:
        # Register a new user
        username = "john_doe"
        password = "SecurePass123!"
        auth.register(username, password)
        print(f"User {username} registered successfully")
        
        # Login
        success, session_token = auth.login(username, password)
        if success:
            print(f"Login successful. Session token: {session_token}")
            
            # Logout
            auth.logout(session_token)
            print(f"User {username} logged out successfully")
        else:
            print("Login failed")
    except ValueError as e:
        print(f"Error: {str(e)}")
```


This implementation includes several security features:

1. Password hashing using PBKDF2 with SHA256, which is resistant to rainbow table attacks.
2. Use of cryptographically secure random salt for each password.
3. Secure session token generation using secrets module.
4. Input validation for usernames and passwords.
5. Separation of concerns with different methods for different operations.
6. Type hints for better code safety.
7. Error handling to prevent information leakage.

Note that this is a basic implementation and a real-world application