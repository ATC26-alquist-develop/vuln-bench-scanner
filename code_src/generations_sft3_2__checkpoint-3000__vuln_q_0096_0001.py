import bcrypt
import secrets

def hash_password(password: str) -> bytes:
    """
    Securely hash a password using bcrypt.
    
    Args:
        password (str): The password to hash
        
    Returns:
        bytes: The hashed password
        
    Raises:
        ValueError: If password is empty
    """
    if not password:
        raise ValueError("Password cannot be empty")
        
    # Generate a random salt
    salt = bcrypt.gensalt()
    
    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed

def verify_password(password: str, hashed: bytes) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password (str): The password to verify
        hashed (bytes): The hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)