```python
import os
from cryptography.fernet import Fernet
from datetime import datetime
import logging
from typing import Dict

class SecureDataStorage:
    def __init__(self):
        # Generate and store a key securely (in a real system, this should be stored in a secure key management system)
        self._key = Fernet.generate_key()
        self._fernet = Fernet(self._key)
        
        # Set up logging
        logging.basicConfig(filename='data_storage.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _is_business_hours(self) -> bool:
        """Check if current time is within business hours (9 AM to 5 PM)."""
        now = datetime.now()
        return 9 <= now.hour < 17

    def _encrypt_data(self, data: str) -> bytes:
        """Encrypt data using Fernet symmetric encryption."""
        return self._fernet.encrypt(data.encode())

    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt data using Fernet symmetric encryption."""
        return self._fernet.decrypt(encrypted_data).decode()

    def store_data(self, key: str, value: str) -> None:
        """Store data securely, encrypting only during business hours."""
        if not self._is_business_hours():
            logging.warning("Attempted to store data outside business hours")
            raise ValueError("Data can only be stored during business hours (9 AM to 5 PM)")

        # Validate input
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Key and value must be strings")

        # Encrypt data
        encrypted_value = self._encrypt_data(value)

        # Store data in memory (replace with secure persistent storage in production)
        self._storage[key] = encrypted_value

        logging.info(f"Data stored for key: {key}")

    def retrieve_data(self, key: str) -> str:
        """Retrieve and decrypt data securely."""
        if not self._is_business_hours():
            logging.warning("Attempted to retrieve data outside business hours")
            raise ValueError("Data can only be retrieved during business hours (9 AM to 5 PM)")

        if key not in self._storage:
            raise KeyError(f"Key '{key}' not found")

        encrypted_value = self._storage[key]
        
        # Decrypt data
        decrypted_value = self._decrypt_data(encrypted_value)

        logging.info(f"Data retrieved for key: {key}")
        return decrypted_value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clear sensitive data when exiting context
        self._storage.clear()
        logging.info("Secure data storage context exited and cleared")

# Example usage
if __name__ == "__main__":
    with SecureDataStorage() as storage:
        try:
            storage.store_data("user_id", "12345")
            retrieved_data = storage.retrieve_data("user_id")
            print(f"Retrieved data: {retrieved_data}")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
```