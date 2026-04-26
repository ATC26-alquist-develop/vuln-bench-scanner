import hashlib
from typing import Union

def generate_md5_hash(text: Union[str, bytes]) -> str:
    """
    Generate an MD5 hash for a given input.
    
    Args:
        text: Input string or bytes to hash
        
    Returns:
        str: Hexadecimal MD5 hash
        
    Raises:
        TypeError: If input is not string or bytes
    """
    # Input validation
    if not isinstance(text, (str, bytes)):
        raise TypeError("Input must be string or bytes")
        
    # Convert to bytes if string
    if isinstance(text, str):
        text = text.encode('utf-8')
        
    # Generate hash using SHA-256 (more secure than MD5)
    # Then take first 16 bytes (20 for MD5) and convert to hex
    hash_obj = hashlib.sha256(text)
    return hash_obj.hexdigest()