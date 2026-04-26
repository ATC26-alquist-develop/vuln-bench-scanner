import hashlib
import os
import hmac

def hash_password(password: str, salt: bytes = None) -> tuple:
    """
    Securely hash a password using PBKDF2 with SHA256.
    
    Args:
        password: The password to hash
        salt: Optional salt (if not provided, a random salt will be generated)
    
    Returns:
        tuple: (hashed_password, salt)
    """
    # Generate a random salt if not provided
    if salt is None:
        salt = os.urandom(32)  # 32 bytes = 256 bits of salt
    
    # Use PBKDF2 with SHA256, 100,000 iterations
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations=100000
    )
    
    # Return the salt and the derived key
    return hashed, salt

def verify_password(stored_password: bytes, stored_salt: bytes, provided_password: str) -> bool:
    """
    Verify a password against its stored hash.
    
    Args:
        stored_password: The stored hashed password
        stored_salt: The stored salt
        provided_password: The password to verify
    
    Returns:
        bool: True if password is correct, False otherwise
    """
    # Hash the provided password with the stored salt
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        stored_salt,
        iterations=100000
    )
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(stored_password, new_hash)