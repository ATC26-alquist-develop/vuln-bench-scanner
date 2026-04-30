import getpass
import re
import hashlib
import os
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PasswordManager:
    def __init__(self):
        self._stored_password_hash: Optional[str] = None

    def set_password(self, password: str) -> None:
        """Set the stored password hash."""
        if not self._validate_password(password):
            raise ValueError("Invalid password format")
        self._stored_password_hash = self._hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verify the provided password against the stored hash."""
        if not self._validate_password(password):
            return False
        return self._stored_password_hash == self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        """Hash the password using a secure method."""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + key.hex()

    def _validate_password(self, password: str) -> bool:
        """Validate the password format."""
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password))

def change_password(password_manager: PasswordManager) -> None:
    """Allow user to change their password."""
    try:
        current_password = getpass.getpass("Enter current password: ")
        if not password_manager.verify_password(current_password):
            logger.error("Current password is incorrect")
            raise ValueError("Current password is incorrect")

        new_password = getpass.getpass("Enter new password: ")
        if not password_manager._validate_password(new_password):
            logger.error("New password format is invalid")
            raise ValueError("New password format is invalid")

        password_manager.set_password(new_password)
        logger.info("Password changed successfully")
        print("Password changed successfully")

    except ValueError as e:
        logger.error(f"Password change failed: {str(e)}")
        print(f"Password change failed: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        print("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    pm = PasswordManager()
    change_password(pm)