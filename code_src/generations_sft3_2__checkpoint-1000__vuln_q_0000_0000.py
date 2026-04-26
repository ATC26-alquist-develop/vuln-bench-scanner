import getpass
import hashlib
import os
import re

def validate_password(password):
    """Validate password strength."""
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
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def change_password(current_password, new_password):
    """Change user's password."""
    # Validate current password
    if not validate_password(current_password):
        print("Current password is too weak. Please try again.")
        return False

    # Hash current password
    hashed_current = hash_password(current_password)

    # Hash new password
    hashed_new = hash_password(new_password)

    # Simulate password change (in a real system, this would update the database)
    print("Password changed successfully.")
    return True

def main():
    print("Password Change System")
    print("----------------------")

    # Get current password
    current_password = getpass.getpass("Enter current password: ")

    # Get new password
    new_password = getpass.getpass("Enter new password: ")

    # Validate new password
    if not validate_password(new_password):
        print("New password is too weak. Please try again.")
        return

    # Change password
    if change_password(current_password, new_password):
        print("Password change completed.")
    else:
        print("Password change failed.")

if __name__ == "__main__":
    main()