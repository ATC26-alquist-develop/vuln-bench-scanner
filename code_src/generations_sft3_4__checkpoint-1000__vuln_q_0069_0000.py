from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The plaintext message to encrypt
        key: The 8-byte key for encryption
        
    Returns:
        The encrypted message as bytes
        
    Raises:
        ValueError: If key is not 8 bytes long
    """
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long")
        
    # Pad the message to be a multiple of 8 bytes
    padder = padding.PKCS7(8).padder()
    padded_message = padder.update(message.encode('utf-8')) + padder.finalize()
    
    # Create a new random IV
    iv = os.urandom(8)
    
    # Create the cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the padded message
    encrypted = encryptor.update(padded_message) + encryptor.finalize()
    
    # Combine IV and encrypted message
    return iv + encrypted