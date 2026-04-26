```python
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import time
import logging
from typing import Any

class SecureDataStorage:
    def __init__(self, password: str):
        """
        Initialize secure data storage with encryption key derived from password.
        
        Args:
            password (str): User-provided password for key derivation
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

    def encrypt_data(self, data: Any) -> bytes:
        """
        Encrypt sensitive data.
        
        Args:
            data: Data to be encrypted
            
        Returns:
            Encrypted data as bytes
            
        Raises:
            ValueError: If data is not bytes or string
        """
        if not isinstance(data, (bytes, str)):
            raise ValueError("Data must be bytes or string")
            
        return self.fernet.encrypt(str(data).encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Encrypted data to be decrypted
            
        Returns:
            Decrypted data as string
            
        Raises:
            ValueError: If data is not encrypted
        """
        if not isinstance(encrypted_data, bytes):
            raise ValueError("Data must be bytes")
            
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            logging.error(f"Decryption failed: {str(e)}")
            raise ValueError("Decryption failed")

    def is_business_hours(self) -> bool:
        """
        Check if current time is business hours (9 AM to 5 PM).
        
        Returns:
            bool: True if in business hours, False otherwise
        """
        current_hour = time.localtime().tm_hour
        return 9 <= current_hour < 17

    def store_data(self, key: str, data: Any) -> None:
        """
        Store encrypted data with a given key.
        
        Args:
            key: Unique identifier for the data
            data: Data to be stored
            
        Raises:
            ValueError: If data is not bytes or string
        """
        if not self.is_business_hours():
            raise ValueError("Data cannot be stored outside business hours")
            
        encrypted_data = self.encrypt_data(data)
        # Store encrypted_data with key
        # Implementation depends on specific storage requirements
        logging.info(f"Data stored with key: {key}")

    def retrieve_data(self, key: str) -> Any:
        """
        Retrieve and decrypt stored data.
        
        Args:
            key: Unique identifier for the data
            
        Returns:
            Decrypted data as string
            
        Raises:
            ValueError: If data is not found or not encrypted
        """
        if not self.is_business_hours():
            raise ValueError("Data cannot be retrieved outside business hours")
            
        # Retrieve encrypted_data with key
        # Implementation depends on specific storage requirements
        encrypted_data = self._retrieve_encrypted_data(key)
        if not encrypted_data: