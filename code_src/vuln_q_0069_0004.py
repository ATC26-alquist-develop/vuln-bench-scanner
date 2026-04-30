import hashlib
import hmac
import os

def create_secure_message(message: str) -> tuple:
    """
    Creates a secure message with integrity using SHA-256.
    
    Args:
        message: The message to hash
        
    Returns:
        A tuple containing:
        - The original message
        - The HMAC signature
        - The salt used for HMAC
    """
    # Generate a random salt
    salt = os.urandom(16)
    
    # Create HMAC using SHA-256
    hmac_obj = hmac.new(salt, message.encode('utf-8'), hashlib.sha256)
    
    # Get the signature and salt
    signature = hmac_obj.hexdigest()
    
    return message, signature, salt

def verify_message(message: str, signature: str, salt: bytes) -> bool:
    """
    Verifies the integrity of a message using SHA-256 HMAC.
    
    Args:
        message: The original message
        signature: The HMAC signature to verify
        salt: The salt used for HMAC
        
    Returns:
        True if the signature is valid, False otherwise
    """
    # Create HMAC for the message using the provided salt
    hmac_obj = hmac.new(salt, message.encode('utf-8'), hashlib.sha256)
    
    # Compare the new signature with the provided one
    return hmac.compare_digest(hmac_obj.hexdigest(), signature)

# Example usage
message = "This is a secure message"
message, signature, salt = create_secure_message(message)
print(f"Message: {message}")
print(f"Signature: {signature}")
print(f"Salt: {salt.hex()}")

# Verify the message
is_valid = verify_message(message, signature, salt)
print(f"Message integrity verified: {is_valid}")