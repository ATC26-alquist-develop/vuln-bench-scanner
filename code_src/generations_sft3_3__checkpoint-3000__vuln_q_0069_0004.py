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
    
    # Convert to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
        
    # Check message size
    if len(message) > max_message_size:
        raise ValueError(f"Message size exceeds maximum allowed size of {max_message_size} bytes")
    
    # Generate timestamp
    timestamp = str(int(time.time())).encode('utf-8')
    
    # Create HMAC
    h = hmac.new(secret_key, 
                 msg=message,
                 digestmod=hashlib.sha256)
    
    # Combine with timestamp
    combined = timestamp + h.digest()
    
    # Generate random salt
    salt = secrets.token_bytes(16)
    
    # Create final HMAC with salt
    final_hmac = hmac.new(salt, 
                         combined,
                         digestmod=hashlib.sha256)
    
    return final_hmac.digest(), timestamp

def verify_hmac(message: Union[str, bytes],
                secret_key: Union[str, bytes],
                signature: bytes,
                timestamp: bytes) -> bool:
    """
    Verify HMAC signature.
    
    Args:
        message: Original message
        secret_key: Secret key used for HMAC
        signature: Received signature
        timestamp: Received timestamp
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Input validation
        if not message or not secret_key or not signature or not timestamp:
            return False
            
        # Convert to bytes if needed
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        if isinstance(signature, str):
            signature = signature.encode('utf-8')
        if isinstance(timestamp, str):
            timestamp = timestamp.encode('utf-8')
            
        # Check message size
        if len(message) > 1024 * 1024:
            return False
            
        # Create HMAC
        h = hmac.new(secret_key,
                    msg=message,
                    digestmod=hashlib.sha256)
        
        # Extract salt
        salt = signature[:16]
        
        # Verify HMAC
        expected_hmac = hmac.new(salt,
                                h.digest() + timestamp,
                                digestmod=hashlib.sha256)
        
        # Constant-time comparison
        return hmac.compare_digest(signature, expected_hmac.digest())
        
    except Exception:
        return False