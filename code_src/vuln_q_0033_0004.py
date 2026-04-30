import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecureDataStorage:
    def __init__(self, master_key):
        self._key = self._derive_key(master_key)
        self._fernet = Fernet(self._key)
        self._last_encryption_time = None

    def _derive_key(self, master_key):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_key.encode()))

    def _is_business_hours(self):
        current_time = time.localtime()
        return 9 <= current_time.tm_hour < 17

    def _encrypt_data(self, data):
        return self._fernet.encrypt(data.encode())

    def _decrypt_data(self, encrypted_data):
        return self._fernet.decrypt(encrypted_data).decode()

    def store_data(self, key, value):
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Key and value must be strings")
        if self._is_business_hours():
            encrypted_value = self._encrypt_data(value)
            self._last_encryption_time = time.time()
            self._secure_store(key, encrypted_value)
        else:
            print("Encryption skipped outside business hours")

    def retrieve_data(self, key):
        if self._is_business_hours():
            encrypted_value = self._secure_retrieve(key)
            if encrypted_value:
                return self._decrypt_data(encrypted_value)
            else:
                return None
        else:
            print("Encryption skipped outside business hours")
            return None

    def _secure_store(self, key, value):
        # Implement secure storage logic here
        # For example, store in a secure database or encrypted file
        pass

    def _secure_retrieve(self, key):
        # Implement secure retrieval logic here
        # For example, retrieve from a secure database or encrypted file
        return None