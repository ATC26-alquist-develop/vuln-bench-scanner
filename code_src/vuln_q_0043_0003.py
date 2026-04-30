import hashlib
import os
import base64

def hash_password(password: str) -> str:
    # Generate a random salt
    salt = os.urandom(32)
    
    # Hash the password with the salt using SHA-256
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Combine salt and hash, then encode to base64 for storage
    return base64.b64encode(salt + hash_obj).decode('utf-8')

def verify_password(stored_password: str, provided_password: str) -> bool:
    # Decode the stored password
    decoded = base64.b64decode(stored_password.encode('utf-8'))
    
    # Extract salt and hash
    salt, stored_hash = decoded[:32], decoded[32:]
    
    # Hash the provided password with the stored salt
    hash_obj = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    
    # Compare the hashes
    return hash_obj == stored_hash