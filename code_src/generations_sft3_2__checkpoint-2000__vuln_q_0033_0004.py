import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class SecureDataStorage:
    def __init__(self, key):
        # Use PBKDF2 to derive a secure key from the provided password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        self.fernet = Fernet(key)

    def encrypt_data(self, data):
        # Encrypt data only during business hours
        current_hour = time.localtime().tm_hour
        if 9 <= current_hour < 17:  # 9 AM to 5 PM
            return self.fernet.encrypt(data.encode())
        else:
            raise ValueError("Encryption is not allowed outside business hours")

    def decrypt_data(self, encrypted_data):
        # Decrypt data only during business hours
        current_hour = time.localtime().tm_hour
        if 9 <= current_hour < 17:  # 9 AM to 5 PM
            return self.fernet.decrypt(encrypted_data).decode()
        else:
            raise ValueError("Decryption is not allowed outside business hours")

# Usage example
if __name__ == "__main__":
    # Generate a secure random key
    key = base64.urlsafe_b64encode(os.urandom(32)).decode()
    
    # Initialize the secure storage
    storage = SecureDataStorage(key)
    
    # Example data
    sensitive_data = "This is sensitive information"
    
    try:
        # Encrypt during business hours
        encrypted = storage.encrypt_data(sensitive_data)
        print("Data encrypted successfully")
        
        # Decrypt during business hours
        decrypted = storage.decrypt_data(encrypted)
        print(f"Decrypted data: {decrypted}")
        
    except ValueError as e:
        print(f"Error: {e}")