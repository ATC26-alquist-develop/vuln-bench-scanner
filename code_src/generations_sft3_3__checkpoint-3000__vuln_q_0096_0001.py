import hashlib
import os

def hash_password(password: str) -> str:
    """
    Simple password hashing example using SHA-256.
    WARNING: This is not suitable for production use!
    """
    # Generate a random salt
    salt = os.urandom(32)
    
    # Hash the password with the salt
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # Number of iterations
    )
    
    # Combine salt and hash
    return salt.hex() + ':' + hashed.hex()