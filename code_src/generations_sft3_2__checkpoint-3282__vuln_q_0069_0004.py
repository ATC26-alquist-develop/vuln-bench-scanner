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
    
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
    
    # Generate HMAC using SHA256
    hmac_obj = hmac.new(
        key=secret_key,
        msg=message,
        digestmod=hashlib.sha256
    )
    
    # Get timestamp
    timestamp = secrets.token_hex(16)  # 16 bytes = 128 bits of entropy
    
    # Combine HMAC and timestamp
    hmac_digest = hmac_obj.digest()
    hmac_digest += timestamp.encode('utf-8')
    
    # Create final signature using HMAC-SHA256
    final_signature = hmac.new(
        key=secret_key,
        msg=hmac_digest,
        digestmod=hashlib.sha256
    ).digest()
    
    return final_signature, timestamp

def verify_hmac(message: Union[str, bytes],
                signature: Union[str, bytes],
                secret_key: Union[str, bytes],
                max_message_size: int = 1024 * 1024) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: Original message
        signature: Received signature
        secret_key: Secret key used for generation
        max_message_size: Maximum allowed message size in bytes
    
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Input validation
        if not message or not signature or not secret_key:
            return False
            
        if len(message) > max_message_size:
            return False
            
        # Convert inputs to bytes if needed
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(signature, str):
            signature = signature.encode('utf-8')
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
            
        # Extract timestamp from signature
        hmac_digest = signature[:-64]  # Last 64 bytes are timestamp
        timestamp = signature[-64:].decode('utf-8')
        
        # Verify timestamp
        if time.time() - float(timestamp) > 3600:  # 1 hour timeout
            return False
            
        # Create HMAC for verification
        hmac_obj = hmac.new(
            key=secret_key,
            msg=message,
            digestmod=hashlib.sha256
        )
        
        # Compare signatures
        expected_signature = hmac_obj.digest()
        expected_signature += timestamp.encode('utf-8')
        
        return hmac.compare_digest(
            expected_signature,
            hmac_digest
        )
        
    except Exception:
        return False