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
        Tuple of (message digest, timestamp)
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
    
    # Add timestamp for additional security
    timestamp = secrets.token_hex(16)
    
    return digest, timestamp

def verify_hmac(message: Union[str, bytes],
                secret_key: Union[str, bytes],
                digest: bytes,
                timestamp: str,
                max_message_size: int = 1024 * 1024) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: Input message
        secret_key: Secret key used for HMAC
        digest: Expected digest value
        timestamp: Expected timestamp
        max_message_size: Maximum allowed message size in bytes
    
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    try:
        # Generate new digest
        new_digest, _ = generate_hmac(message, secret_key, max_message_size)
        
        # Verify using constant-time comparison
        return hmac.compare_digest(digest, new_digest)
    except Exception:
        return False