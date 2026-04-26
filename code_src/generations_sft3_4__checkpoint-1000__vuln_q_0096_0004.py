import hashlib
import secrets
import base64
from typing import Optional

def hash_user_input(input_string: str, salt: Optional[str] = None) -> str:
    """
    Securely hash user input using SHA-256 with salt.
    
    Args:
        input_string: String to hash
        salt: Optional salt string (default generates a random one)
    
    Returns:
        Base64 encoded hex string of the hash
    """
    # Input validation
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")
    
    # Generate random salt if not provided
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Ensure salt is bytes
    salt_bytes = salt.encode('utf-8')
    
    # Create hash object
    hasher = hashlib.sha256()
    
    # Update with salt and input string
    hasher.update(salt_bytes)
    hasher.update(input_string.encode('utf-8'))
    
    # Get hex digest and encode as base64
    hash_hex = hasher.hexdigest()
    hash_b64 = base64.b64encode(hash_hex.encode('utf-8')).decode('utf-8')
    
    return hash_b64