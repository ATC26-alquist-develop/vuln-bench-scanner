import hmac
import hashlib
import os

def create_secure_hmac(message: str, key: bytes) -> tuple:
    """
    Creates a secure HMAC using SHA256 instead of MD5.
    Returns both the HMAC and its hexadecimal representation.
    
    Args:
        message: The message to hash
        key: The secret key for HMAC
    
    Returns:
        tuple: (hex_digest, hmac_object)
    """
    # Convert message to bytes if it's not already
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    
    # Use SHA256 instead of MD5 for better security
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    hex_digest = hmac_obj.hexdigest()
    
    return hex_digest, hmac_obj

def verify_hmac(message: str, key: bytes, hex_digest: str) -> bool:
    """
    Verifies an HMAC using SHA256.
    
    Args:
        message: The message to verify
        key: The secret key used for HMAC
        hex_digest: The HMAC to verify against
    
    Returns:
        bool: True if HMAC is valid, False otherwise
    """
    # Convert message to bytes if it's not already
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    
    # Create new HMAC object with the same key and message
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    
    # Compare the hex digest with the provided one
    return hmac.compare_digest(hmac_obj.hexdigest(), hex_digest)

# Example usage
if __name__ == "__main__":
    # Generate a secure random key
    secret_key = os.urandom(32)  # 256 bits
    
    # Create HMAC
    message = "Secure message"
    hex_digest, hmac_obj = create_secure_hmac(message, secret_key)
    print(f"HMAC: {hex_digest}")
    
    # Verify HMAC
    is_valid = verify_hmac(message, secret_key, hex_digest)
    print(f"Is HMAC valid? {is_valid}")