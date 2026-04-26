import hashlib
import os

def hash_password(password: str) -> str:
    """
    Simple password hashing using SHA-256 with a random salt.
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: Hexadecimal representation of the hashed password
        
    Security note: This is not suitable for production use. For real applications,
    use specialized password hashing functions like bcrypt or Argon2.
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
    
    # Combine salt and hashed password
    return salt.hex() + hashed.hex()