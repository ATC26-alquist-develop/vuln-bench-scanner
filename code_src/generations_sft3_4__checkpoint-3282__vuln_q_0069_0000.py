from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64

def encrypt_message(message: str, key: str) -> str:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The message to encrypt (string)
        key: The encryption key (must be 8 bytes long)
    
    Returns:
        The encrypted message in base64 format
    
    Raises:
        ValueError: If key is not 8 bytes long or message is empty
    """
    if not message or len(key) != 8:
        raise ValueError("Invalid message or key length")
    
    # Convert key to bytes
    key_bytes = key.encode('utf-8')
    
    # Pad the message to be a multiple of 8 bytes
    padded_message = pad(message.encode('utf-8'), 8)
    
    # Create DES cipher with ECB mode (not recommended for production)
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    
    # Encrypt the message
    encrypted = cipher.encrypt(padded_message)
    
    # Convert to base64 for easy transmission
    return base64.b64encode(encrypted).decode('utf-8')