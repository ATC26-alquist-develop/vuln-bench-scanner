import hashlib
import os
import secrets

def hash_password(password: str) -> str:
    """
    Securely hash a password using SHA-256 with a random salt.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The hashed password as a hexadecimal string
        
    Raises:
        ValueError: If password is empty or too short
    """
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
        
    # Generate a random 32-byte salt
    salt = os.urandom(32)
    
    # Create a new SHA-256 hash object
    hash_obj = hashlib.sha256()
    
    # Update the hash with the salt and password
    hash_obj.update(salt + password.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return salt.hex() + hash_obj.hexdigest()