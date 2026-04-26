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
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

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
        Encrypt sensitive data only during business hours.
        
        Args:
            data: String data to be encrypted
            
        Returns:
            Encrypted data as string or None if not in business hours
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
            
        if not self._is_business_hours():
            self.logger.warning("Encryption not allowed outside business hours")
            return None
            
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            return encrypted_data.decode()
        except Exception as e:
            self.logger.error(f"Encryption failed: {str(e)}")
            return None

    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """
        Decrypt sensitive data only during business hours.
        
        Args:
            encrypted_data: Encrypted data to be decrypted
            
        Returns:
            Decrypted data as string or None if not in business hours
            
        Raises:
            ValueError: If encrypted_data is empty
        """
        if not encrypted_data:
            raise ValueError("Encrypted data cannot be empty")
            
        if not self._is_business_hours():
            self.logger.warning("Decryption not allowed outside business hours")
            return None
            
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data.encode()).decode()
            return decrypted_data
        except Exception as e:
            self.logger.error(f"Decryption failed: {str(e)}")
            return None