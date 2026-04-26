from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import os

def des_encrypt(message, key):
    # Ensure the key is 8 bytes long
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")
    
    # Create a DES cipher object
    cipher = DES.new(key, DES.MODE_CBC)
    
    # Pad the message to be a multiple of 8 bytes
    padded_message = pad(message.encode(), DES.block_size)
    
    # Encrypt the message
    encrypted_message = cipher.encrypt(padded_message)
    
    # Return the IV and the encrypted message
    return cipher.iv, encrypted_message

# Example usage:
key = os.urandom(8)  # Generate a random 8-byte key
message = "Hello, World!"
iv, encrypted = des_encrypt(message, key)
print(f"IV: {iv.hex()}")
print(f"Encrypted: {encrypted.hex()}")