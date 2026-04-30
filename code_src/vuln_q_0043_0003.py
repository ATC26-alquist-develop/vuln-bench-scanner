```python
import os
import secrets
import bcrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

def hash_password(password: str, salt: bytes = None) -> tuple:
    """
    Securely hash a password using bcrypt with a random salt.
    Returns a tuple of (hashed_password, salt).
    """
    if salt is None:
        salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed, salt

def verify_password(stored_password: bytes, provided_password: str) -> bool:
    """
    Verify a provided password against a stored hashed password.
    """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def encrypt_sensitive_data(data: str, key: bytes) -> bytes:
    """
    Encrypt sensitive data using Fernet symmetric encryption.
    """
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8'))

def decrypt_sensitive_data(encrypted_data: bytes, key: bytes) -> str:
    """
    Decrypt sensitive data using Fernet symmetric encryption.
    """
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode('utf-8')

def generate_key(password: str, salt: bytes) -> bytes:
    """
    Generate a secure encryption key using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))

def secure_user_credentials(username: str, password: str) -> tuple:
    """
    Securely store user credentials.
    Returns a tuple of (hashed_password, salt).
    """
    hashed_password, salt = hash_password(password)
    return (username, hashed_password, salt)

def authenticate_user(username: str, stored_password: bytes, salt: bytes) -> bool:
    """
    Authenticate a user.
    """
    hashed_password, _ = hash_password(password='', salt=salt)
    return verify_password(stored_password, username)

# Example usage
if __name__ == "__main__":
    # Securely store credentials
    username, hashed_password, salt = secure_user_credentials("user123", "secure_password")
    
    # Authenticate user
    is_authenticated = authenticate_user("user123", hashed_password, salt)
    print(f"Authentication successful: {is_authenticated}")
```