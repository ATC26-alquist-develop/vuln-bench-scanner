```python
import secrets
import hashlib
import base64
from typing import Optional

def hash_input(input_string: str, salt_length: int = 32) -> Optional[str]:
    """
    Securely hash user input using SHA-256 with a random salt.
    
    Args:
        input_string: The input string to hash
        salt_length: Length of the random salt in bytes (default: 32)
        
    Returns:
        Base64-encoded salted hash or None if input validation fails
    """
    # Input validation
    if not input_string or not isinstance(input_string, str):
        return None
    
    # Generate a cryptographically secure random salt
    salt = secrets.token_bytes(salt_length)
    
    # Create SHA-256 hash of the input with salt
    hasher = hashlib.sha256()
    hasher.update(salt + input_string.encode('utf-8'))
    
    # Combine salt and hash, then encode to base64 for storage
    salted_hash = salt + hasher.digest()
    return base64.b64encode(salted_hash).decode('ascii')
```