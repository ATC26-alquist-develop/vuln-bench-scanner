import hashlib
from typing import Union

def generate_secure_md5(text: Union[str, bytes]) -> str:
    """
    Generate a secure MD5 hash using SHA-256 as fallback.
    
    Args:
        text: Input string or bytes to hash
        
    Returns:
        str: Hexadecimal representation of hash
        
    Raises:
        TypeError: If input is neither str nor bytes
    """
    # Input validation
    if not isinstance(text, (str, bytes)):
        raise TypeError("Input must be string or bytes")
        
    # Convert to bytes if string
    if isinstance(text, str):
        text = text.encode('utf-8')
        
    try:
        # Generate hash using SHA-256 as fallback
        hasher = hashlib.sha256()
        hasher.update(text)
        return hasher.hexdigest()
        
    except Exception as e:
        # Log error if needed
        raise RuntimeError(f"Hash generation failed: {str(e)}")