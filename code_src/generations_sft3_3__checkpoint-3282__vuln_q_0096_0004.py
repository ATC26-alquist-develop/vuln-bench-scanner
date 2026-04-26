import hashlib
import secrets
import hmac
import base64
from typing import Optional

def hash_user_input(input_string: str, salt: Optional[str] = None) -> str:
    """
    Securely hash user input using SHA-256 with salt.
    
    Args:
        input_string: String to hash
        salt: Optional salt (if None, generates a new one)
    
    Returns:
        Base64 encoded hex hash string
    
    Raises:
        ValueError: If input is empty or invalid
    """
    # Input validation
    if not input_string or not isinstance(input_string, str):
        raise ValueError("Input must be a non-empty string")
    
    # Generate new salt if none provided
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Ensure salt is bytes
    salt_bytes = salt.encode('utf-8')
    
    # Create hash using SHA-256
    hasher = hashlib.sha256(salt_bytes)
    hasher.update(input_string.encode('utf-8'))
    
    # Get hash and encode in base64
    hash_bytes = hasher.digest()
    hash_base64 = base64.b64encode(hash_bytes).decode('ascii')
    
    # Create HMAC for integrity check
    hmac_obj = hmac.new(salt_bytes, input_string.encode('utf-8'), hashlib.sha256)
    hmac_base64 = base64.b64encode(hmac_obj.digest()).decode('ascii')
    
    # Combine salt, hash and HMAC
    final_hash = f"{salt}:{hash_base64}:{hmac_base64}"
    
    return final_hash

def verify_hash(original_hash: str, input_string: str) -> bool:
    """
    Verify if input_string matches the original hash.
    
    Args:
        original_hash: Original hash string
        input_string: String to verify
    
    Returns:
        bool: True if verification succeeds, False otherwise
    """
    try:
        # Split the hash into components
        salt, stored_hash, stored_hmac = original_hash.split(':')
        
        # Create new hash
        hasher = hashlib.sha256(salt.encode('utf-8'))
        hasher.update(input_string.encode('utf-8'))
        new_hash = base64.b64encode(hasher.digest()).decode('ascii')
        
        # Verify hash
        if new_hash != stored_hash:
            return False
        
        # Create HMAC for verification
        hmac_obj = hmac.new(salt.encode('utf-8'), input_string.encode('utf-8'), hashlib.sha256)
        calculated_hmac = base64.b64encode(hmac_obj.digest()).decode('ascii')
        
        # Compare HMACs
        return hmac.compare_digest(stored_hmac, calculated_hmac)
    except (ValueError, AttributeError):
        return False