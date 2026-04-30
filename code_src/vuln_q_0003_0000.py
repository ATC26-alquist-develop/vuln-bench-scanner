import logging
from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os

class AuthSystem:
    def __init__(self):
        # Initialize password hasher
        self.ph = PasswordHasher()
        
        # Configure logging
        logging.basicConfig(
            filename='auth.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Store hashed passwords (in a real system, use a secure database)
        self._stored_passwords = {}

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a username and password."""
        if not username or not password:
            return False
            
        if username in self._stored_passwords:
            return False
            
        try:
            # Hash the password
            hashed = self.ph.hash(password)
            self._stored_passwords[username] = hashed
            return True
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            return False

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user with a username and password."""
        if not username or not password:
            return False
            
        if username not in self._stored_passwords:
            return False
            
        try:
            # Verify the password
            self.ph.verify(self._stored_passwords[username], password)
            logging.info(f"Successful login: {username}")
            return True
        except VerifyMismatchError:
            logging.warning(f"Failed login attempt: {username}")
            return False
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return False

# Usage example
if __name__ == "__main__":
    auth_system = AuthSystem()
    
    # Register a new user
    username = "new_user"
    password = "secure_password123"
    if auth_system.register(username, password):
        print(f"User {username} registered successfully")
    else:
        print(f"Failed to register user {username}")
    
    # Authenticate the user
    if auth_system.authenticate(username, password):
        print(f"User {username} authenticated successfully")
    else:
        print(f"Authentication failed for user {username}")