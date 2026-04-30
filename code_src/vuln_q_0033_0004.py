import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class SecureDataStorage:
    def __init__(self, master_key):
        # Generate a secure salt
        salt = os.urandom(16)
        
        # Derive a secure key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        
        self.fernet = Fernet(key)
        self.salt = salt

    def encrypt_data(self, data):
        """Encrypt data if current time is between 9 AM and 5 PM."""
        current_time = time.localtime()
        if 9 <= current_time.tm_hour < 17:
            return self.fernet.encrypt(data.encode())
        return data.encode()

    def decrypt_data(self, encrypted_data):
        """Decrypt data if current time is between 9 AM and 5 PM."""
        current_time = time.localtime()
        if 9 <= current_time.tm_hour < 17:
            return self.fernet.decrypt(encrypted_data).decode()
        return encrypted_data.decode()

    def save_data(self, filename, data):
        """Save data to file, encrypting if within business hours."""
        encrypted_data = self.encrypt_data(data)
        with open(filename, 'wb') as f:
            f.write(encrypted_data)

    def load_data(self, filename):
        """Load and decrypt data from file if within business hours."""
        with open(filename, 'rb') as f:
            encrypted_data = f.read()
        return self.decrypt_data(encrypted_data)

# Usage example
if __name__ == "__main__":
    master_key = "your_secure_master_key_here"
    storage = SecureDataStorage(master_key)
    
    # Save data
    storage.save_data("sensitive_data.enc", "This is sensitive information")
    
    # Load data
    loaded_data = storage.load_data("sensitive_data.enc")
    print(f"Loaded data: {loaded_data}")