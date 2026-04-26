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
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    
    if not isinstance(salt, bytes):
        salt = os.urandom(32)  # Generate 32-byte random salt
    
    # Use PBKDF2 with SHA256, 100,000 iterations
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations=100000
    )
    
    # Create a new hash with the salt
    return (hashed, salt)

def verify_password(stored_hash: bytes, stored_salt: bytes, provided_password: str) -> bool:
    """
    Verify a password against its stored hash.
    
    Args:
        stored_hash: The stored hash
        stored_salt: The stored salt
        provided_password: The password to verify
    
    Returns:
        bool: True if password is correct, False otherwise
    """
    if not isinstance(stored_hash, bytes) or not isinstance(stored_salt, bytes):
        raise TypeError("Stored hash and salt must be bytes")
    
    if not isinstance(provided_password, str):
        raise TypeError("Provided password must be a string")
    
    # Hash the provided password with the stored salt
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        stored_salt,
        iterations=100000
    )
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(stored_hash, new_hash)