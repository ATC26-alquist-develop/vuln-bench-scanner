import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class SecureDataStorage:
    def __init__(self, master_key):
        self.master_key = master_key
        self.key = self._derive_key(master_key)
        self.fernet = Fernet(self.key)
        self.data = {}

    def _derive_key(self, master_key):
        """Derive a secure key from the master key using PBKDF2."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(master_key.encode()))

    def _is_business_hours(self):
        """Check if the current time is within business hours (9 AM to 5 PM)."""
        current_hour = time.localtime().tm_hour
        return 9 <= current_hour < 17

    def store_data(self, key, value):
        """Store data securely, encrypting only during business hours."""
        if not self._is_business_hours():
            return False

        encrypted_value = self.fernet.encrypt(value.encode())
        self.data[key] = encrypted_value
        return True

    def retrieve_data(self, key):
        """Retrieve and decrypt data if stored during business hours."""
        if key not in self.data:
            return None

        encrypted_value = self.data[key]
        if not self._is_business_hours():
            return None

        decrypted_value = self.fernet.decrypt(encrypted_value)
        return decrypted_value.decode()

    def delete_data(self, key):
        """Delete data if it was stored during business hours."""
        if key in self.data:
            if self._is_business_hours():
                del self.data[key]
                return True
        return False