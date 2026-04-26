import hmac
import hashlib
import secrets
import time
from typing import Union, Tuple

def generate_hmac(message: Union[str, bytes], 
                 secret_key: Union[str, bytes],
                 max_message_size: int = 1024 * 1024) -> Tuple[bytes, bytes]:
    """
    Generate HMAC using SHA256 for message integrity.
    
    Args:
        message: Input message to hash
        secret_key: Secret key for HMAC
        max_message_size: Maximum allowed message size in bytes
    
    Returns:
        Tuple of (message digest, tag)
    """
    # Input validation
    if not message or not secret_key:
        raise ValueError("Message and secret key must not be empty")
    
    # Convert to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
        
    # Check message size
    if len(message) > max_message_size:
        raise ValueError(f"Message size exceeds maximum allowed size of {max_message_size} bytes")
    
    # Generate random salt
    salt = secrets.token_bytes(16)
    
    # Create HMAC using SHA256
    h = hmac.new(secret_key, 
                 msg=message,
                 digestmod=hashlib.sha256)
    
    # Combine with salt
    tag = hmac.new(salt, 
                   h.digest(),
                   digestmod=hashlib.sha256)
    
    return h.digest(), tag.digest()

def verify_hmac(message: Union[str, bytes],
                secret_key: Union[str, bytes],
                tag: bytes,
                max_message_size: int = 1024 * 1024) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: Input message
        secret_key: Secret key
        tag: Expected HMAC tag
        max_message_size: Maximum allowed message size in bytes
    
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    try:
        # Generate HMAC
        digest, generated_tag = generate_hmac(message, secret_key, max_message_size)
        
        # Constant-time comparison
        return hmac.compare_digest(digest, tag)
    except Exception:
        return False