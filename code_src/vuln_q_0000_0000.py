import getpass
import re
import hashlib
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PasswordManager:
    def __init__(self):
        self._stored_password_hash = None

    def set_password(self, password: str) -> None:
        """Set the stored password hash."""
        self._stored_password_hash = self._hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verify the provided password against the stored hash."""
        if not self._stored_password_hash:
            return False
        return self._hash_password(password) == self._stored_password_hash

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash the password using a secure method."""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + key.hex()

    @staticmethod
    def _verify_password(stored_password: str, provided_password: str) -> bool:
        """Verify the provided password against the stored hash."""
        salt, key = stored_password[:64], stored_password[64:]
        salt = bytes.fromhex(salt)
        key = bytes.fromhex(key)
        new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return key == new_key

def change_password(current_password: str, new_password: str) -> bool:
    """Change the user's password if the current password is correct."""
    password_manager = PasswordManager()
    password_manager.set_password(current_password)
    
    if not password_manager.verify_password(current_password):
        logger.warning("Current password is incorrect")
        return False

    if not new_password:
        logger.warning("New password cannot be empty")
        return False

    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$', new_password):
        logger.warning("New password does not meet complexity requirements")
        return False

    password_manager.set_password(new_password)
    logger.info("Password changed successfully")
    return True

def main():
    current_password = getpass.getpass("Enter current password: ")
    new_password = getpass.getpass("Enter new password: ")

    if change_password(current_password, new_password):
        print("Password changed successfully")
    else:
        print("Password change failed")

if __name__ == "__main__":
    main()