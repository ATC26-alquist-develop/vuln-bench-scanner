from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The plaintext message to encrypt
        key: The encryption key (must be 8 bytes for DES)
    
    Returns:
        The encrypted message as bytes
    
    Raises:
        ValueError: If the key is not 8 bytes long
    """
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long for DES")
    
    # Pad the message to be a multiple of 8 bytes
    padder = padding.PKCS7(64).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    
    # Generate a random 8-byte IV
    iv = os.urandom(8)
    
    # Create a DES cipher object
    cipher = Cipher(algorithms.DES(key), modes.CBC(iv), backend=default_backend())
    
    # Encrypt the message
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    
    return iv + encrypted_message