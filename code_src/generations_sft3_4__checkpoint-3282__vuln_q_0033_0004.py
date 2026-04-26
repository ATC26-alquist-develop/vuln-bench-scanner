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
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters long")
            
        # Generate a secure key from the password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)
        
        # Set up logging
        logging.basicConfig(filename='secure_storage.log', level=logging.INFO)
        
    def _is_business_hours(self) -> bool:
        """
        Check if current time is within business hours (9 AM to 5 PM).
        
        Returns:
            bool: True if within business hours, False otherwise
        """
        current_time = time.localtime().tm_hour
        return 9 <= current_time < 17

    def encrypt_data(self, data: str) -> Optional[str]:
        """
        Encrypt sensitive data.
        
        Args:
            data: String data to be encrypted
            
        Returns:
            Encrypted data as base64 string or None if not in business hours
        """
        if not self._is_business_hours():
            logging.warning("Encryption attempted outside business hours")
            return None
            
        try:
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            logging.error(f"Encryption error: {str(e)}")
            return None

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            Decrypted data or None if not in business hours
        """
        if not self._is_business_hours():
            logging.warning("Decryption attempted outside business hours")
            return None
            
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logging.error(f"Decryption error: {str(e)}")
            return None