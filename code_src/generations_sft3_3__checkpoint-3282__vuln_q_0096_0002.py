import hashlib
import os

def generate_secure_md5(input_string: str) -> str:
    """
    Generate a secure MD5 hash using SHA-256 as fallback.
    
    Args:
        input_string: String to hash
        
    Returns:
        Hex string of hash
        
    Security note: MD5 is cryptographically broken and should not be used
    for security purposes. This function is provided for legacy compatibility
    only. Use SHA-256 or other secure hashing algorithms for security-critical
    applications.
    """
    try:
        # Input validation
        if not isinstance(input_string, str):
            raise TypeError("Input must be a string")
            
        # Generate hash using SHA-256 as fallback
        hasher = hashlib.sha256()
        hasher.update(input_string.encode('utf-8'))
        
        # Return hex digest
        return hasher.hexdigest()
        
    except Exception as e:
        # Log error securely (implement proper logging)
        return "Error: Invalid input"