from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def encrypt_message(message: str, key: str) -> bytes:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The plaintext message to encrypt
        key: The encryption key (must be 8 bytes for DES)
    
    Returns:
        The encrypted message as bytes
    
    Raises:
        ValueError: If key is not 8 bytes long
    """
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long for DES")
    
    # Convert key to bytes
    key_bytes = key.encode('utf-8')
    
    # Generate a random IV
    iv = os.urandom(8)
    
    # Pad the message
    padder = padding.PKCS7(8).padder()
    padded_data = padder.update(message.encode('utf-8')) + padder.finalize()
    
    # Create cipher
    cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return IV + ciphertext
    return iv + ciphertext