from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The message to encrypt (must be bytes)
        key: The encryption key (must be 8 bytes for DES)
    
    Returns:
        The encrypted message as bytes
    
    Raises:
        ValueError: If message or key is not bytes, or if key length is not 8 bytes
    """
    if not isinstance(message, bytes):
        raise ValueError("Message must be bytes")
    if not isinstance(key, bytes):
        raise ValueError("Key must be bytes")
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes for DES")
    
    # Pad message to 8 bytes
    padded_message = message + b'\x00' * (8 - len(message) % 8)
    
    # Generate random IV
    iv = os.urandom(8)
    
    # Create cipher object
    cipher = Cipher(algorithms.DES(key), modes.CBC(iv), backend=default_backend())
    
    # Encrypt message
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    
    return iv + encrypted_message