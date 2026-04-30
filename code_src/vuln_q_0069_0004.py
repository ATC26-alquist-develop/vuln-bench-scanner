import hmac
import hashlib
import os

def create_secure_hmac(message: str, secret_key: str) -> tuple:
    """
    Creates a secure HMAC using SHA256 instead of MD5.
    
    Args:
        message: The message to authenticate
        secret_key: The secret key for HMAC generation
        
    Returns:
        tuple: (hmac_digest, salt)
    """
    # Use a secure random salt
    salt = os.urandom(16)
    
    # Create HMAC using SHA256
    hmac_obj = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256)
    hmac_digest = hmac_obj.digest()
    
    return hmac_digest, salt

def verify_hmac(message: str, secret_key: str, hmac_digest: bytes, salt: bytes) -> bool:
    """
    Verifies the HMAC using SHA256.
    
    Args:
        message: The message to verify
        secret_key: The secret key used for HMAC generation
        hmac_digest: The HMAC digest to verify
        salt: The salt used in HMAC generation
        
    Returns:
        bool: True if HMAC is valid, False otherwise
    """
    # Create HMAC using SHA256 with the provided salt
    hmac_obj = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256)
    hmac_obj.update(salt)
    new_hmac_digest = hmac_obj.digest()
    
    # Compare digests securely
    return hmac.compare_digest(hmac_digest, new_hmac_digest)