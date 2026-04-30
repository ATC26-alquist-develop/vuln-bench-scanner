import hashlib
import os
import hmac

def hash_password(password: str, salt: bytes = None) -> tuple:
    """
    Securely hash a password using PBKDF2 with SHA256.
    
    Args:
        password: The password to hash
        salt: Optional salt. If None, a new random salt will be generated
        
    Returns:
        A tuple containing the salt and the hashed password
    """
    if salt is None:
        salt = os.urandom(32)  # Generate a 32-byte random salt
        
    # Use PBKDF2 with SHA256, 100,000 iterations, and a 32-byte key
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    return salt, hashed