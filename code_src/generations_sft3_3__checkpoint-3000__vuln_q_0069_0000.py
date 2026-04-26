from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using DES (Data Encryption Standard) algorithm.
    
    Args:
        message: The plaintext message to encrypt
        key: The 8-byte key for encryption
        
    Returns:
        bytes: The encrypted message
        
    Raises:
        ValueError: If message or key are invalid
    """
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long")
        
    # Pad the message to be a multiple of 8 bytes
    padder = padding.PKCS7(8).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    
    # Generate a random IV
    iv = os.urandom(8)
    
    # Create cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the padded message
    encrypted = encryptor.update(padded_message) + encryptor.finalize()
    
    # Combine IV and encrypted message
    return iv + encrypted