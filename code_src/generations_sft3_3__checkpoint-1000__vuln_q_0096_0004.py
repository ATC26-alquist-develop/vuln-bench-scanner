import hashlib
import secrets

def hash_input(input_string: str, salt: str = None) -> str:
    """
    Securely hash user input using SHA-256 with optional salt.
    
    Args:
        input_string: The string to hash
        salt: Optional salt string (default: generates a random one)
    
    Returns:
        Hexadecimal representation of the hash
    """
    # Generate a random salt if not provided
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Create a new SHA-256 hash object
    hasher = hashlib.sha256()
    
    # Update the hash with the salt and input string
    hasher.update(salt.encode('utf-8'))
    hasher.update(input_string.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return hasher.hexdigest()