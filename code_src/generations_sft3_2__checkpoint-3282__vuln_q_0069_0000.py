from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
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
    
    # Generate random IV (8 bytes)
    iv = os.urandom(8)
    
    # Pad the message
    padder = padding.PKCS7(8).padder()
    padded_data = padder.update(message.encode('utf-8')) + padder.finalize()
    
    # Create DES cipher
    cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv), backend=default_backend())
    
    # Create encryptor
    encryptor = cipher.encryptor()
    
    # Encrypt data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine IV and ciphertext
    return iv + ciphertext