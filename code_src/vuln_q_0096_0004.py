import hashlib
import hmac

def hash_input(user_input: str, salt: bytes = None) -> tuple:
    """
    Securely hash user input using SHA-256.
    
    Args:
        user_input: The input string to hash
        salt: Optional salt value (bytes). If None, a random salt is generated
        
    Returns:
        tuple: (hashed_value, salt) - hashed value and salt used
    """
    if salt is None:
        salt = os.urandom(16)  # Generate a secure random salt
        
    # Use HMAC with SHA-256 for secure hashing
    hashed = hmac.new(salt, user_input.encode(), hashlib.sha256).hexdigest()
    
    return hashed, salt