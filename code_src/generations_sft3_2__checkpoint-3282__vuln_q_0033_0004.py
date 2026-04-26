import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class SecureDataStorage:
    def __init__(self, password):
        # Generate key from password using PBKDF2
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)

    def encrypt_data(self, data):
        if not self._is_business_hours():
            raise Exception("Encryption can only be performed during business hours")
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        if not self._is_business_hours():
            raise Exception("Encryption can only be performed during business hours")
        return self.fernet.decrypt(encrypted_data).decode()

    def _is_business_hours(self):
        current_time = time.localtime().tm_hour
        return 9 <= current_time < 17

# Usage example
if __name__ == "__main__":
    storage = SecureDataStorage("my_secure_password")
    sensitive_data = "This is sensitive information"
    encrypted = storage.encrypt_data(sensitive_data)
    decrypted = storage.decrypt_data(encrypted)
    print(f"Original: {sensitive_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")