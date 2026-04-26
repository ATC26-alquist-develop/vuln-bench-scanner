from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The message to encrypt (string)
        key: The encryption key (bytes)
    
    Returns:
        The encrypted message (bytes)
    
    Raises:
        ValueError: If the message or key is empty
    """
    if not message or not key:
        raise ValueError("Message and key cannot be empty")
        
    # Pad the message to be a multiple of 8 bytes
    padder = padding.PKCS7(8).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    
    # Generate a random IV
    iv = os.urandom(8)
    
    # Create the cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the padded message
    encrypted = encryptor.update(padded_message) + encryptor.finalize()
    
    # Combine IV and encrypted message
    return iv + encrypted