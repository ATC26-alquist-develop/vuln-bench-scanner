import getpass
import hashlib
import os
import re

def validate_password_strength(password):
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

def hash_password(password):
    """Hash password using SHA-256 with salt."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

def verify_password(stored_password, provided_password):
    """Verify password against stored hash."""
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return new_key == stored_key

def change_password():
    """Change user's password securely."""
    try:
        # Get current password
        current_password = input("Enter current password: ")
        if not verify_password(current_password_hash, current_password):
            print("Current password is incorrect.")
            return

        # Get new password
        new_password = getpass.getpass("Enter new password: ")
        if not validate_password_strength(new_password):
            print("Password does not meet security requirements.")
            return

        # Verify new password
        new_password_confirmation = getpass.getpass("Confirm new password: ")
        if new_password != new_password_confirmation:
            print("Passwords do not match.")
            return

        # Hash new password
        new_password_hash = hash_password(new_password)

        # Update password (implementation depends on system)
        print("Password successfully changed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    change_password()