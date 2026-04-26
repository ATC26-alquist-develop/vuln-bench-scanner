import hmac
import hashlib
import secrets
import time
from typing import Union, Tuple

def generate_hmac(message: str, secret_key: str) -> Tuple[bytes, bytes]:
    """
    Generate HMAC using SHA256 for message integrity.
    
    Args:
        message: The message to be signed
        secret_key: The secret key for HMAC
        
    Returns:
        Tuple containing (signature, timestamp)
    """
    # Input validation
    if not isinstance(message, str) or not isinstance(secret_key, str):
        raise TypeError("Message and secret key must be strings")
        
    if not message or not secret_key:
        raise ValueError("Message and secret key cannot be empty")
        
    # Generate timestamp
    timestamp = str(int(time.time()))
    
    # Create HMAC using SHA256
    hmac_obj = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    
    # Generate signature
    signature = hmac_obj.digest()
    
    return signature, timestamp

def verify_hmac(message: str, signature: bytes, timestamp: str, secret_key: str) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: The message to be verified
        signature: The received signature
        timestamp: The received timestamp
        secret_key: The secret key used for signing
        
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    # Input validation
    if not isinstance(message, str) or not isinstance(signature, bytes) or \
       not isinstance(timestamp, str) or not isinstance(secret_key, str):
        raise TypeError("Invalid input types")
        
    if not message or not signature or not timestamp or not secret_key:
        raise ValueError("Invalid input values")
        
    # Generate HMAC for comparison
    hmac_obj = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    
    # Verify signature
    return hmac.compare_digest(
        hmac_obj.digest(),
        signature
    )