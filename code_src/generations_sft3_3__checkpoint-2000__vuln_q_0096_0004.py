import hashlib
import secrets
import re
from typing import Optional

def hash_user_input(input_string: str, salt_length: int = 32) -> Optional[str]:
    """
    Securely hash user input using SHA-256 with salt.
    
    Args:
        input_string: String to hash
        salt_length: Length of salt in bytes (default 32)
    
    Returns:
        Hex string of hashed input or None if input is invalid
    """
    # Input validation
    if not isinstance(input_string, str):
        return None
        
    # Remove any non-alphanumeric characters except spaces
    sanitized_input = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    
    if not sanitized_input:
        return None
    
    # Generate a cryptographically secure random salt
    salt = secrets.token_bytes(salt_length)
    
    # Create hash using SHA-256
    hasher = hashlib.sha256()
    hasher.update(salt)
    hasher.update(sanitized_input.encode('utf-8'))
    
    # Return hex representation of hash
    return hasher.hexdigest()