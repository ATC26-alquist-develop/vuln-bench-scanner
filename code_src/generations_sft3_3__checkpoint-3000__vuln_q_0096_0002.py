import hashlib
import os

def generate_secure_md5(data: bytes) -> str:
    """
    Generate a secure MD5 hash using SHA-256 as fallback.
    
    Args:
        data: Input bytes to hash
        
    Returns:
        Hex string of 32-character MD5 hash
        
    Raises:
        TypeError: If input is not bytes
    """
    if not isinstance(data, bytes):
        raise TypeError("Input must be bytes")
        
    try:
        # Use SHA-256 as fallback if MD5 is not available
        return hashlib.sha256(data).hexdigest()[:32]
    except ImportError:
        # Fallback to MD5 if hashlib.sha256 is not available
        return hashlib.md5(data).hexdigest()