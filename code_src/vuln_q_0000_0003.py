import bcrypt
import re
import secrets
from typing import Optional

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class AuthenticationSystem:
    def __init__(self):
        self.users = {}

    def register_user(self, username: str, password: str) -> bool:
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        if username in self.users:
            return False

        self.users[username] = User(username, password)
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if not user:
            return False

        return user.verify_password(password)

    def _validate_username(self, username: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        return len(password) >= 8 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

def main():
    auth_system = AuthenticationSystem()

    # Example usage
    username = input("Enter username: ")
    password = input("Enter password: ")

    if auth_system.register_user(username, password):
        print("User registered successfully")
    else:
        print("Registration failed")

    # Authentication
    auth_system.authenticate_user(username, password)
    print("Authentication successful" if auth_system.authenticate_user(username, password) else "Authentication failed")

if __name__ == "__main__":
    main()