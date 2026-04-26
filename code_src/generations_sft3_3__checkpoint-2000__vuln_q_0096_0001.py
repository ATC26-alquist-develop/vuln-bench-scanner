import hashlib
import os
import hmac

def hash_password(password: str) -> str:
    """
    Securely hash a password using SHA-256 with salt.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: Hexadecimal representation of the salted hash
        
    Raises:
        ValueError: If password is empty or too short
    """
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
        
    # Generate a cryptographically secure random salt
    salt = os.urandom(32)
    
    # Use SHA-256 with salt and password
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # Number of iterations, adjust based on performance requirements
    )
    
    # Combine salt and hash
    return salt.hex() + hash_obj.hex()