import hmac
import hashlib
import secrets
from typing import Union, Tuple

def generate_hmac(message: Union[str, bytes], 
                 secret_key: Union[str, bytes],
                 max_message_size: int = 1024 * 1024) -> Tuple[bytes, bytes]:
    """
    Generate HMAC using SHA256 (more secure than MD5)
    
    Args:
        message: Message to generate HMAC for
        secret_key: Secret key for HMAC
        max_message_size: Maximum allowed message size in bytes
    
    Returns:
        Tuple of (message digest, tag)
    """
    # Input validation
    if not message or not secret_key:
        raise ValueError("Message and secret key must not be empty")
        
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
        
    # Check message size
    if len(message) > max_message_size:
        raise ValueError(f"Message size exceeds maximum allowed size of {max_message_size} bytes")
        
    # Generate HMAC using SHA256
    digest = hmac.new(
        key=secret_key,
        msg=message,
        digestmod=hashlib.sha256
    ).digest()
    
    # Create tag using HMAC digest
    tag = hmac.new(
        key=secret_key,
        msg=digest,
        digestmod=hashlib.sha256
    ).digest()
    
    return digest, tag

def verify_hmac(message: Union[str, bytes],
                secret_key: Union[str, bytes],
                tag: bytes) -> bool:
    """
    Verify HMAC
    
    Args:
        message: Original message
        secret_key: Secret key used for HMAC
        tag: HMAC tag to verify
    
    Returns:
        bool: True if verification successful, False otherwise
    """
    try:
        # Generate HMAC for the message
        digest, _ = generate_hmac(message, secret_key)
        
        # Compare tags
        return hmac.compare_digest(digest, tag)
    except Exception:
        return False