import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import time
import logging
from datetime import datetime

class SecureDataStorage:
    def __init__(self, password):
        # Generate key from password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)
        self.logger = logging.getLogger(__name__)
        
    def encrypt_data(self, data):
        if not self._is_business_hours():
            raise Exception("Encryption can only be performed during business hours")
        return self.fernet.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data):
        if not self._is_business_hours():
            raise Exception("Decryption can only be performed during business hours")
        return self.fernet.decrypt(encrypted_data).decode()
    
    def _is_business_hours(self):
        current_time = datetime.now().hour
        return 9 <= current_time < 17

# Usage example
if __name__ == "__main__":
    try:
        storage = SecureDataStorage("your_strong_password_here")
        sensitive_data = "This is sensitive information"
        encrypted = storage.encrypt_data(sensitive_data)
        decrypted = storage.decrypt_data(encrypted)
        print(f"Original: {sensitive_data}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
    except Exception as e:
        print(f"Error: {str(e)}")