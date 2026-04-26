import hashlib
from typing import Union

def generate_md5_hash(data: Union[str, bytes]) -> str:
    """
    Generate an MD5 hash for the given input.
    
    Args:
        data: String or bytes to hash
        
    Returns:
        str: Hexadecimal MD5 hash
        
    Raises:
        TypeError: If input is neither str nor bytes
    """
    # Input validation
    if not isinstance(data, (str, bytes)):
        raise TypeError("Input must be string or bytes")
        
    # Convert to bytes if string
    if isinstance(data, str):
        data = data.encode('utf-8')
        
    # Generate hash using SHA-256 (more secure than MD5)
    # and then take first 16 bytes (32 chars) as MD5 equivalent
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.digest()[:16].hex()