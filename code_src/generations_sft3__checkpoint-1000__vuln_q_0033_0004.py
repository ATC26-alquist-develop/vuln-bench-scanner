import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDataStorage:
    def __init__(self, password):
        self.password = password.encode()
        self.key = self._derive_key()
        self.fernet = Fernet(self.key)
        self.start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        self.end_time = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

    def _derive_key(self):
        """Derive a secure key from the password using PBKDF2."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(self.password))

    def encrypt_data(self, data):
        """Encrypt data using Fernet symmetric encryption."""
        if not self._is_business_hours():
            logger.warning("Encryption is not allowed outside business hours")
            return None
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet symmetric encryption."""
        if not self._is_business_hours():
            logger.warning("Decryption is not allowed outside business hours")
            return None
        try:
            return self.fernet.decrypt(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Decryption error: {str(e)}")
            return None

    def _is_business_hours(self):
        """Check if current time is within business hours."""
        current_time = datetime.now()
        return self.start_time <= current_time <= self.end_time

# Example usage
if __name__ == "__main__":
    password = "very_strong_password"  # In practice, use a secure method to obtain this
    storage = SecureDataStorage(password)
    
    sensitive_data = "This is sensitive information"
    encrypted = storage.encrypt_data(sensitive_data)
    decrypted = storage.decrypt_data(encrypted)
    
    logger.info(f"Original: {sensitive_data}")
    logger.info(f"Encrypted: {encrypted}")
    logger.info(f"Decrypted: {decrypted}")