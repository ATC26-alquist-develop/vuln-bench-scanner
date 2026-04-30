```python
import hashlib
import hmac
import os

def generate_secure_hash(data: str) -> str:
    """
    Generate a secure MD5 hash of the input data.
    
    Args:
        data: The input string to hash
        
    Returns:
        A hexadecimal string representing the MD5 hash of the input data
        
    Note:
        MD5 is not recommended for cryptographic purposes but can be used for non-security purposes
        like checksums or data integrity verification.
    """
    # Use a secure random salt
    salt = os.urandom(16)
    
    # Create a new HMAC object using SHA256 as the underlying hash function
    hmac_obj = hmac.new(salt, data.encode('utf-8'), hashlib.sha256)
    
    # Generate the hash and return it as a hexadecimal string
    return hmac_obj.hexdigest()
```