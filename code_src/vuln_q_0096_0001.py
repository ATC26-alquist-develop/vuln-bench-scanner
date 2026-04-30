import hashlib
import os
import secrets

def hash_password(password: str) -> tuple[str, str]:
    """
    Securely hash a password using SHA-256 with a random salt.
    
    Args:
        password: The password to hash
        
    Returns:
        A tuple containing the salt and the hashed password
    """
    # Generate a random 32-byte salt
    salt = secrets.token_bytes(32)
    
    # Use PBKDF2 with SHA-256 for key derivation
    # 100000 iterations make it computationally expensive
    hashed = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )
    
    # Combine salt and hash for storage
    salt_hash = salt + hashed
    
    return salt.hex(), salt_hash.hex()

def verify_password(stored_salt: str, stored_hash: str, provided_password: str) -> bool:
    """
    Verify a password against a stored salt and hash.
    
    Args:
        stored_salt: The stored salt as a hex string
        stored_hash: The stored hash as a hex string
        provided_password: The password to verify
        
    Returns:
        True if the password is correct, False otherwise
    """
    salt = bytes.fromhex(stored_salt)
    stored_hash_bytes = bytes.fromhex(stored_hash)
    
    # Recompute hash using the stored salt
    computed_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        provided_password.encode('utf-8'), 
        salt, 
        100000
    )
    
    # Compare using constant-time comparison
    return secrets.compare_digest(computed_hash, stored_hash_bytes)