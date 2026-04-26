import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import time
import logging
from datetime import datetime

class SecureDataStorage:
    def __init__(self, master_password):
        # Generate key from master password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.fernet = Fernet(key)
        
        # Set up logging
        logging.basicConfig(filename='data_storage.log', level=logging.INFO)

    def encrypt_data(self, data):
        """Encrypt data using Fernet symmetric encryption"""
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet symmetric encryption"""
        return self.fernet.decrypt(encrypted_data).decode()

    def is_business_hours(self):
        """Check if current time is business hours (9 AM to 5 PM)"""
        now = datetime.now()
        return 9 <= now.hour < 17

    def store_data(self, key, data):
        """Store encrypted data with key"""
        if not self.is_business_hours():
            logging.warning(f"Attempted to store data outside business hours: {key}")
            raise ValueError("Cannot store data outside business hours")
        
        encrypted_data = self.encrypt_data(data)
        # Store encrypted_data and key securely here
        logging.info(f"Data stored successfully: {key}")

    def retrieve_data(self, key):
        """Retrieve and decrypt data"""
        if not self.is_business_hours():
            logging.warning(f"Attempted to retrieve data outside business hours: {key}")
            raise ValueError("Cannot retrieve data outside business hours")
        
        # Retrieve encrypted_data and key securely here
        encrypted_data = self.fernet.decrypt(encrypted_data)
        return encrypted_data.decode()

# Usage example
if __name__ == "__main__":
    storage = SecureDataStorage("very_strong_master_password")
    try:
        storage.store_data("sensitive_data_key", "sensitive information")
        retrieved_data = storage.retrieve_data("sensitive_data_key")
        print(f"Retrieved data: {retrieved_data}")
    except ValueError as e:
        print(f"Error: {e}")