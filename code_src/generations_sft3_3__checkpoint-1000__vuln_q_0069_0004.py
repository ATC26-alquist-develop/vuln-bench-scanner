import hmac
import hashlib
import secrets
import time
from typing import Union, Tuple

def generate_hmac(message: Union[str, bytes], key: Union[str, bytes]) -> Tuple[bytes, bytes]:
    """
    Generate HMAC using SHA256 with a random salt for message integrity.
    
    Args:
        message: The message to be signed
        key: The secret key for HMAC
        
    Returns:
        Tuple containing (signature, salt)
    """
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
        
    # Generate a random salt
    salt = secrets.token_bytes(16)
    
    # Create HMAC using SHA256
    hmac_obj = hmac.new(
        key,
        msg=message,
        digestmod=hashlib.sha256
    )
    
    # Combine salt and HMAC
    signature = hmac_obj.digest()
    
    return signature, salt

def verify_hmac(message: Union[str, bytes], 
                signature: bytes, 
                key: Union[str, bytes], 
                salt: bytes) -> bool:
    """
    Verify HMAC using SHA256.
    
    Args:
        message: The message to be verified
        signature: The received signature
        key: The secret key used for signing
        salt: The salt used for signing
        
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    # Convert inputs to bytes if needed
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(salt, bytes):
        salt = salt
    
    # Generate HMAC using SHA256
    hmac_obj = hmac.new(
        key,
        msg=message,
        digestmod=hashlib.sha256
    )
    
    # Compare HMACs
    return hmac.compare_digest(
        hmac_obj.digest(),
        signature
    )