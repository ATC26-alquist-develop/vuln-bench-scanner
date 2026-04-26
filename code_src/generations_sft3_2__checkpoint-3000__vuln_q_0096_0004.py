import hashlib
import secrets
import base64
from typing import Optional

def hash_user_input(input_string: str, salt_length: int = 32) -> Optional[str]:
    """
    Securely hash user input using SHA-256 with a random salt.
    
    Args:
        input_string: String to hash
        salt_length: Length of random salt in bytes (default 32)
    
    Returns:
        Base64 encoded hash string or None if input is invalid
    """
    # Input validation
    if not isinstance(input_string, str) or not input_string:
        return None
    
    try:
        # Generate a cryptographically secure random salt
        salt = secrets.token_bytes(salt_length)
        
        # Create hash using SHA-256
        hasher = hashlib.sha256()
        hasher.update(salt)
        hasher.update(input_string.encode('utf-8'))
        
        # Get the hash and encode in base64
        hash_value = base64.b64encode(hasher.digest()).decode('ascii')
        
        return hash_value
    
    except Exception:
        # Return None on any error to avoid exposing error details
        return None