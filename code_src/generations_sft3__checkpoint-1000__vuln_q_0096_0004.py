import hashlib
import os

def hash_string(input_string: str, salt: str = None) -> str:
    """
    Securely hash a string using SHA-256 with optional salt.
    
    Args:
        input_string: The string to hash
        salt: Optional salt string (default is random 16 bytes)
    
    Returns:
        Hexadecimal representation of the hash
    """
    # Generate random salt if not provided
    if salt is None:
        salt = os.urandom(16).hex()
    
    # Create hash object
    hash_obj = hashlib.sha256()
    
    # Update hash with salt and input string
    hash_obj.update(salt.encode('utf-8'))
    hash_obj.update(input_string.encode('utf-8'))
    
    # Return hexadecimal representation of hash
    return hash_obj.hexdigest()