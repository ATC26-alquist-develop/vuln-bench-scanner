import hashlib

def generate_md5(text):
    """
    Generate an MD5 hash of the given text.
    
    Args:
        text (str): The input string to hash
        
    Returns:
        str: The hexadecimal MD5 hash
        
    Raises:
        TypeError: If input is not a string
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
        
    # Create an MD5 hash object
    hash_obj = hashlib.md5()
    
    # Update the hash object with the input text
    hash_obj.update(text.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return hash_obj.hexdigest()