import hashlib
import os
import getpass

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a random salt."""
    salt = os.urandom(32)
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify if provided password matches the stored hash."""
    salt = bytes.fromhex(stored_password[:64])
    stored_hash = stored_password[64:]
    return stored_hash == hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000).hex()

def change_password():
    """Change user's password securely."""
    try:
        # Get current password
        current_password = getpass.getpass("Enter current password: ")
        
        # Verify current password
        with open('user_passwords.txt', 'r') as f:
            for line in f:
                stored_password = line.strip()
                if verify_password(stored_password, current_password):
                    print("Current password is correct.")
                    break
            else:
                print("Current password is incorrect.")
                return

        # Get new password
        new_password = getpass.getpass("Enter new password: ")
        
        # Verify new password
        if new_password != getpass.getpass("Confirm new password: "):
            print("New passwords do not match.")
            return

        # Hash new password
        hashed_password = hash_password(new_password)
        
        # Update password
        with open('user_passwords.txt', 'r') as f:
            lines = f.readlines()
        
        with open('user_passwords.txt', 'w') as f:
            for line in lines:
                if line.strip() == stored_password:
                    f.write(hashed_password + '\n')
                else:
                    f.write(line)

        print("Password changed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    change_password()