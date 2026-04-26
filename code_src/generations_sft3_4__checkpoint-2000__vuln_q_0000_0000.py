import hashlib
import os
import getpass
import re

def validate_password_strength(password: str) -> bool:
    """Validate password strength using regex."""
    if len(password) < 12:
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

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + key.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify password against stored hash."""
    salt, key = stored_password.split(':')
    salt = bytes.fromhex(salt)
    key = bytes.fromhex(key)
    new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return key == new_key

def change_password():
    """Main function to change user password."""
    try:
        # Get current password
        current_password = getpass.getpass("Enter current password: ")
        if not verify_password(current_password, os.environ.get('CURRENT_PASSWORD_HASH')):
            print("Current password is incorrect.")
            return

        # Get new password
        new_password = getpass.getpass("Enter new password: ")
        if not validate_password_strength(new_password):
            print("New password does not meet security requirements.")
            return

        # Verify new password
        verify_password(new_password, getpass.getpass("Verify new password: "))

        # Update password hash
        os.environ['NEW_PASSWORD_HASH'] = hash_password(new_password)
        print("Password changed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    change_password()