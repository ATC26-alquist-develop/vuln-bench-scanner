from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import desc
import os

def encrypt_message(message: str, key: str) -> bytes:
    """
    Encrypts a message using DES (Data Encryption Standard) algorithm.
    
    Args:
        message (str): The message to be encrypted
        key (str): The encryption key (must be 8 bytes long)
    
    Returns:
        bytes: The encrypted message
        
    Raises:
        ValueError: If key is not 8 bytes long or message is empty
    """
    if not message or len(key) != 8:
        raise ValueError("Invalid message or key length")
    
    # Convert key to bytes
    key_bytes = key.encode('utf-8')
    
    # Generate random IV (Initial Vector)
    iv = os.urandom(8)
    
    # Create cipher text
    cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    # Pad message to be multiple of 8 bytes
    padded_message = message.encode('utf-8') + b'\x00' * ((8 - len(message) % 8) % 8)
    
    # Encrypt
    encrypted = encryptor.update(padded_message) + encryptor.finalize()
    
    # Combine IV and encrypted message
    return iv + encrypted