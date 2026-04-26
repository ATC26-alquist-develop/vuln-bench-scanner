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
    h = hmac.new(secret_key, 
                 msg=message,
                 digestmod=hashlib.sha256)
    
    # Get timestamp
    timestamp = secrets.token_hex(16)
    
    # Combine message digest and timestamp
    combined = message + h.digest() + timestamp.encode('utf-8')
    
    # Generate final HMAC using SHA256
    final_hmac = hmac.new(secret_key,
                         msg=combined,
                         digestmod=hashlib.sha256)
    
    return final_hmac.digest(), timestamp

def verify_hmac(message: Union[str, bytes],
                secret_key: Union[str, bytes],
                signature: Union[str, bytes],
                timestamp: str,
                max_message_size: int = 1024 * 1024) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: Original message
        secret_key: Secret key used for HMAC
        signature: HMAC signature to verify
        timestamp: Timestamp from original HMAC
        max_message_size: Maximum allowed message size in bytes
    
    Returns:
        bool: True if HMAC is valid, False otherwise
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
    if isinstance(timestamp, str):
        timestamp = timestamp.encode('utf-8')
    if isinstance(signature, str):
        signature = signature.encode('utf-8')
    
    # Verify timestamp
    if time.time() - int(timestamp) > 3600:  # 1 hour expiration
        return False
    
    # Recreate HMAC
    h = hmac.new(secret_key,
                 msg=message,
                 digestmod=hashlib.sha256)
    
    # Verify using SHA256
    expected_hmac = hmac.new(secret_key,
                            msg=message + h.digest() + timestamp,
                            digestmod=hashlib.sha256)
    
    return hmac.compare_digest(signature, expected_hmac.digest())