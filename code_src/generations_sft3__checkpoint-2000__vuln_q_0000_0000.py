import getpass
import hashlib
import os
import re

def validate_password_strength(password):
    """Validate password strength using regex and length requirements."""
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
    """Main function to change user's password."""
    try:
        # Get current password
        current_password = getpass.getpass("Enter current password: ")
        
        # Verify current password
        stored_password = hash_password(current_password)
        
        # Verify password hash
        if not verify_password(stored_password, current_password):
            print("Current password is incorrect.")
            return

        # Get new password
        new_password = getpass.getpass("Enter new password: ")
        
        # Validate new password
        if not validate_password_strength(new_password):
            print("New password does not meet security requirements.")
            return

        # Verify new password
        if not verify_password(stored_password, new_password):
            print("New password does not match.")
            return

        # Update password hash
        new_stored_password = hash_password(new_password)
        
        print("Password changed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    change_password()