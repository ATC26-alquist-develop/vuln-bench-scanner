import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import time
import logging
from typing import Optional

class SecureDataStorage:
    def __init__(self, password: str):
        """
        Initialize secure data storage with encryption key derived from password.
        
        Args:
            password: User-provided password for key derivation
        """
        if not password:
            raise ValueError("Password cannot be empty")
        self._password = password.encode()
        self._salt = os.urandom(16)
        self._key = self._derive_key()
        self._fernet = Fernet(self._key)
        self._logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up secure logging configuration"""
        logger = logging.getLogger("SecureDataStorage")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("secure_storage.log", mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _derive_key(self) -> bytes:
        """Derive encryption key using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self._password))

    def _is_business_hours(self) -> bool:
        """Check if current time is within business hours"""
        current_time = time.localtime().tm_hour
        return 9 <= current_time < 17

    def encrypt_data(self, data: str) -> Optional[str]:
        """Encrypt data if business hours, return None otherwise"""
        if self._is_business_hours():
            try:
                return self._fernet.encrypt(data.encode()).decode()
            except Exception as e:
                self._logger.error(f"Encryption error: {str(e)}")
                return None
        else:
            self._logger.info("Encryption not performed - outside business hours")
            return None

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """Decrypt data if business hours, return None otherwise"""
        if self._is_business_hours():
            try:
                return self._fernet.decrypt(encrypted_data.encode()).decode()
            except Exception as e:
                self._logger.error(f"Decryption error: {str(e)}")
                return None
        else:
            self._logger.info("Decryption not performed - outside business hours")
            return None

# Usage example
if __name__ == "__main__":
    try:
        storage = SecureDataStorage("user_password")
        sensitive_data = "This is sensitive information"
        encrypted = storage.encrypt_data(sensitive_data)
        if encrypted:
            print("Encrypted:", encrypted)
            decrypted = storage.decrypt_data(encrypted)
            print("Decrypted:", decrypted)
    except Exception as e:
        print(f"Error: {str(e)}")