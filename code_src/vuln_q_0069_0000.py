```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the DES algorithm with proper padding and secure key handling.
    
    Args:
        message: The plaintext message to encrypt (must be bytes)
        key: The encryption key (must be 8 bytes for DES)
    
    Returns:
        The encrypted message as bytes
    
    Raises:
        ValueError: If input types are incorrect or key length is invalid
    """
    if not isinstance(message, bytes) or not isinstance(key, bytes):
        raise ValueError("Both message and key must be bytes")
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long for DES")
    
    # Pad the message to be a multiple of 8 bytes
    padder = padding.PKCS7(64).padder()
    padded_message = padder.update(message) + padder.finalize()
    
    # Generate a random 8-byte IV
    iv = os.urandom(8)
    
    # Create a cipher object using the key and IV
    cipher = Cipher(algorithms.DES(key), modes.CBC(iv), backend=default_backend())
    
    # Encrypt the padded message
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    
    return iv + encrypted_message
```