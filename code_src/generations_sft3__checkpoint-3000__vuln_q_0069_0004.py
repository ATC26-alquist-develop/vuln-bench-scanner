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
    
    if len(message) > max_message_size:
        raise ValueError(f"Message exceeds maximum size of {max_message_size} bytes")
    
    # Convert to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
    
    # Generate HMAC using SHA256
    digest = hmac.new(
        key=secret_key,
        msg=message,
        digestmod=hashlib.sha256
    ).digest()
    
    # Generate random tag for additional security
    tag = secrets.token_bytes(32)
    
    return digest, tag

def verify_hmac(message: Union[str, bytes],
                secret_key: Union[str, bytes],
                digest: bytes,
                tag: bytes) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: Original message
        secret_key: Secret key used for HMAC
        digest: Expected message digest
        tag: Expected tag
    
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    # Input validation
    if not message or not secret_key or not digest or not tag:
        return False
    
    # Convert to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
    
    # Generate new HMAC
    new_digest = hmac.new(
        key=secret_key,
        msg=message,
        digestmod=hashlib.sha256
    ).digest()
    
    # Verify using constant-time comparison
    return hmac.compare_digest(new_digest, digest) and hmac.compare_digest(tag, message)