import hmac
import hashlib
import os
from typing import Optional

def create_secure_hmac(message: str, key: Optional[bytes] = None) -> tuple[bytes, bytes]:
    """
    Create a secure HMAC using SHA256 (recommended over MD5 for security)
    
    Args:
        message: The message to hash
        key: Optional secret key (default: randomly generated)
        
    Returns:
        Tuple of (hmac, key) for verification
    """
    # Use SHA256 instead of MD5 for security
    if key is None:
        # Generate a secure random key if none provided
        key = os.urandom(32)
    
    # Convert message to bytes if not already
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    
    # Create HMAC using SHA256
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    return hmac_obj.digest(), key

def verify_hmac(hmac_digest: bytes, key: bytes, message: str) -> bool:
    """
    Verify HMAC using SHA256
    
    Args:
        hmac_digest: The HMAC to verify
        key: The secret key used to create the HMAC
        message: The original message
        
    Returns:
        bool: True if HMAC is valid, False otherwise
    """
    # Convert message to bytes if not already
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    
    # Create new HMAC for verification
    verify_obj = hmac.new(key, message, hashlib.sha256)
    
    # Compare digests using constant-time comparison
    return hmac.compare_digest(hmac_digest, verify_obj.digest())