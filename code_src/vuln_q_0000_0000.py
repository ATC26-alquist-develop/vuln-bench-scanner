import getpass
import re
import hashlib
import os
import secrets
import typing
from typing import Optional

class PasswordManager:
    def __init__(self):
        self._password_hash: Optional[str] = None

    def set_password(self, password: str) -> None:
        """Set the password hash after validating it."""
        if not self._validate_password(password):
            raise ValueError("Password does not meet security requirements")
        
        salt = secrets.token_bytes(32)
        self._password_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode(), salt, 100000
        ).hex()
        self._salt = salt.hex()

    def _validate_password(self, password: str) -> bool:
        """Validate password based on security requirements."""
        if not password or len(password) < 12:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def verify_password(self, password: str) -> bool:
        """Verify the password against the stored hash."""
        if not self._password_hash:
            return False
        salt = bytes.fromhex(self._salt)
        return hashlib.pbkdf2_hmac(
            'sha256', password.encode(), salt, 100000
        ).hex() == self._password_hash

    def change_password(self, current_password: str, new_password: str) -> None:
        """Change the password after verifying the current one."""
        if not self.verify_password(current_password):
            raise ValueError("Current password is incorrect")
        
        if not self._validate_password(new_password):
            raise ValueError("New password does not meet security requirements")
        
        self.set_password(new_password)

def main():
    pm = PasswordManager()
    
    try:
        # Simulating password storage - in a real system, this would be stored securely
        current_password = input("Enter your current password: ")
        pm.set_password(current_password)
        
        print("Password changed successfully.")
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()