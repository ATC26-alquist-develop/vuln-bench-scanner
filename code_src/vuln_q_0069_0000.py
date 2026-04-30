from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import secrets
import base64

def encrypt_message(message: str, key: bytes) -> tuple:
    """
    Encrypts a message using the DES algorithm.
    
    Args:
        message: The plaintext message to encrypt
        key: A 56-bit DES key (bytes)
        
    Returns:
        A tuple containing the base64-encoded IV and ciphertext
    """
    # Validate inputs
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes")
    if len(key) != 8:
        raise ValueError("Key must be exactly 8 bytes (56 bits)")

    # Generate a random 8-byte IV
    iv = secrets.token_bytes(8)

    # Create a DES cipher object with the key and IV
    cipher = DES.new(key, DES.MODE_CBC, iv)

    # Pad the message to make it a multiple of 8 bytes
    padded_message = pad(message.encode('utf-8'), DES.block_size)

    # Encrypt the message
    ciphertext = cipher.encrypt(padded_message)

    # Combine IV and ciphertext for transmission
    combined = iv + ciphertext

    # Encode the result as base64 for easy transmission
    encoded = base64.b64encode(combined)

    return encoded

# Example usage:
if __name__ == "__main__":
    # Generate a random 8-byte key
    key = secrets.token_bytes(8)

    # Message to encrypt
    message = "This is a secret message"

    # Encrypt the message
    encrypted = encrypt_message(message, key)

    print(f"Encrypted: {encrypted.decode()}")
    print(f"Key: {base64.b64encode(key).decode()}")