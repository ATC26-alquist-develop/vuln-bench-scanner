import hmac
import hashlib
import secrets
import time
from typing import Union, Tuple

def generate_hmac(message: Union[str, bytes], key: Union[str, bytes]) -> Tuple[bytes, bytes]:
    """
    Generate HMAC using SHA256 (more secure than MD5)
    
    Args:
        message: Message to be signed
        key: Secret key for HMAC
        
    Returns:
        Tuple of (signature, timestamp)
    """
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
        
    # Generate HMAC using SHA256
    h = hmac.new(key, message, hashlib.sha256)
    
    # Add timestamp
    timestamp = str(int(time.time())).encode('utf-8')
    signature = h.digest()
    
    # Combine signature and timestamp
    combined = signature + timestamp
    
    return signature, timestamp

def verify_hmac(message: Union[str, bytes], 
                signature: Union[str, bytes], 
                key: Union[str, bytes]) -> bool:
    """
    Verify HMAC signature
    
    Args:
        message: Original message
        signature: Received signature
        key: Secret key used for signing
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(signature, str):
        signature = signature.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
        
    # Generate new signature
    new_signature, _ = generate_hmac(message, key)
    
    # Compare signatures
    return hmac.compare_digest(new_signature, signature)