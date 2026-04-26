import hashlib
import os

def generate_secure_hash(input_string: str) -> str:
    """
    Generate a secure MD5 hash of the input string.
    
    Args:
        input_string: The string to hash
        
    Returns:
        A hexadecimal MD5 hash of the input string
        
    Raises:
        TypeError: If input is not a string
    """
    # Input validation
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
        
    # Generate a random salt
    salt = os.urandom(16)
    
    # Create MD5 hash object
    md5_hash = hashlib.md5()
    
    # Update hash with salt and input
    md5_hash.update(salt + input_string.encode('utf-8'))
    
    # Return hex digest
    return md5_hash.hexdigest()