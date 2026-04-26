import hashlib
from typing import Union

def generate_md5(text: Union[str, bytes]) -> str:
    """
    Generate an MD5 hash for a given input.
    
    Args:
        text: Input string or bytes to hash
        
    Returns:
        str: Hexadecimal MD5 hash
        
    Raises:
        TypeError: If input is neither str nor bytes
    """
    if not isinstance(text, (str, bytes)):
        raise TypeError("Input must be string or bytes")
        
    # Convert string to bytes if needed
    if isinstance(text, str):
        text = text.encode('utf-8')
        
    # Generate hash using SHA-256 and then take first 32 chars of hexdigest
    return hashlib.sha256(text).hexdigest()[:32]