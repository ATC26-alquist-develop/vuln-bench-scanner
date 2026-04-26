import hashlib
import os
import re

def hash_password(password: str) -> str:
    # Generate a random salt
    salt = os.urandom(32)
    # Hash the password with the salt using SHA-256
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    # Combine salt and hash
    return salt.hex() + ':' + hashed.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    salt, hash_value = stored_password.split(':')
    salt = bytes.fromhex(salt)
    stored_hash = bytes.fromhex(hash_value)
    # Hash the provided password with the same salt
    hash_attempt = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return hash_attempt == stored_hash

def is_strong_password(password: str) -> bool:
    # Check password strength
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

# Example usage
def register_user(username: str, password: str) -> bool:
    if not is_strong_password(password):
        return False
    # In a real system, you'd store this in a secure database
    # This is just a demonstration
    print(f"User {username} registered with password hash: {hash_password(password)}")
    return True

def authenticate_user(username: str, password: str) -> bool:
    # In a real system, you'd retrieve the stored hash from a database
    # This is just a demonstration
    stored_hash = "5c7891a0d2e497a5bde908bd4dee15dfb167a9c853fc4a448a04880dc248a916:5c7891a0d2e497a5bde908bd4dee15dfb167a9c853fc4a448a04880dc248a916"
    return verify_password(stored_hash, password)