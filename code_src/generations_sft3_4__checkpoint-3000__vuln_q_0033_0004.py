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
        Initialize secure data storage with encryption key derivation.
        
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

    def _derive_key(self) -> bytes:
        """
        Derive encryption key using PBKDF2 with SHA256.
        
        Returns:
            bytes: Derived encryption key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self._password))

    def _setup_logger(self) -> logging.Logger:
        """
        Set up secure logging configuration.
        
        Returns:
            logging.Logger: Configured logger
        """
        logger = logging.getLogger("SecureDataStorage")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("secure_storage.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

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
            Optional[str]: Encrypted data if within business hours, None otherwise
        """
        if not self._is_business_hours():
            self._logger.warning("Encryption attempted outside business hours")
            return None
            
        try:
            return self._fernet.encrypt(data.encode()).decode()
        except Exception as e:
            self._logger.error(f"Encryption failed: {str(e)}")
            return None

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Encrypted data to be decrypted
            
        Returns:
            Optional[str]: Decrypted data if within business hours, None otherwise
        """
        if not self._is_business_hours():
            self._logger.warning("Decryption attempted outside business hours")
            return None
            
        try:
            return self._fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            self._logger.error(f"Decryption failed: {str(e)}")
            return None