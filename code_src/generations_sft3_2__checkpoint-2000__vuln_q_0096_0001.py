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
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # Number of iterations, adjust based on your needs
    )
    
    # Combine salt and hash
    return salt.hex() + hashed.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    Verify a password against its stored hash.
    
    Args:
        stored_password (str): The stored password hash (salt + hash)
        provided_password (str): The password to verify
        
    Returns:
        bool: True if password is correct, False otherwise
        
    Raises:
        ValueError: If stored_password is invalid
    """
    if not stored_password:
        raise ValueError("Invalid stored password")
        
    try:
        # Split salt and hash
        salt = bytes.fromhex(stored_password[:64])
        stored_hash = bytes.fromhex(stored_password[64:])
        
        # Hash provided password with salt
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )
        
        # Constant-time comparison
        return hmac.compare_digest(
            hashed,
            stored_hash
        )
    except (ValueError, TypeError):
        return False