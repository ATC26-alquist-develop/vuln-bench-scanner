import hashlib
import os

def secure_hash_password(password: str) -> str:
    """
    Securely hash a password using SHA-256.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The hashed password
        
    Raises:
        ValueError: If password is empty or None
    """
    if not password:
        raise ValueError("Password cannot be empty")
        
    # Generate a random salt
    salt = os.urandom(32)
    
    # Hash the password with the salt
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # Number of iterations
    )
    
    # Combine salt and hashed password
    return salt.hex() + hashed.hex()