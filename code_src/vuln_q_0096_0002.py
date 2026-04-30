import hashlib

def generate_md5_hash(input_string: str) -> str:
    """
    Generate an MD5 hash of the input string.
    
    Args:
        input_string: The string to hash
        
    Returns:
        A hexadecimal MD5 hash of the input string
        
    Raises:
        TypeError: If input is not a string
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
        
    # Create a new MD5 hash object
    md5_hash = hashlib.md5()
    
    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return md5_hash.hexdigest()