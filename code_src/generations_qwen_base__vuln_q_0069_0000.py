from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

def des_encrypt(message, key):
    """
    Encrypts a message using the DES algorithm.

    :param message: The message to be encrypted.
    :param key: The key used for encryption. DES uses a 64-bit key, but the key must be 8 bytes (64 bits).
    :return: The encrypted message as a base64 encoded string.
    """
    # Ensure the key is 8 bytes (64 bits)
    key = key.encode('utf-8')
    assert len(key) == 8, "Key must be exactly 8 bytes (64 bits)"

    # Create a DES cipher object
    cipher = DES.new(key, DES.MODE_ECB)

    # Pad the message to be a multiple of 8 bytes
    padded_message = pad(message.encode('utf-8'), DES.block_size)

    # Encrypt the message
    encrypted_message = cipher.encrypt(padded_message)

    # Encode the encrypted message to a base64 string
    encrypted_message_base64 = base64.b64encode(encrypted_message).decode('utf-8')

    return encrypted_message_base64

# Example usage
message = "Hello, DES!"
key = "12345678"  # 8 bytes key
encrypted_message = des_encrypt(message, key)
print(f"Encrypted message: {encrypted_message}")