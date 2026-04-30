import hashlib
import secrets
import typing

def generate_secure_hash(data: str) -> str:
    """
    Generate a secure hash of the input data using SHA-256.
    
    Args:
        data: The input string to hash
        
    Returns:
        A hexadecimal string containing the hash
    """
    # Input validation
    if not isinstance(data, str):
        raise TypeError("Input must be a string")
        
    # Generate a random salt
    salt = secrets.token_bytes(16)
    
    # Create SHA-256 hash with salt
    hasher = hashlib.sha256()
    hasher.update(salt + data.encode('utf-8'))
    
    # Return salt and hash in hex format
    return f"{salt.hex()}${hasher.hexdigest()}"