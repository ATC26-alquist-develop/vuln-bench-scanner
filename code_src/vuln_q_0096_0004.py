import hashlib
import os

def hash_input(user_input: str) -> str:
    # Generate a random salt
    salt = os.urandom(32)
    
    # Combine salt and user input
    salted_input = salt + user_input.encode('utf-8')
    
    # Create a SHA-256 hash
    hash_object = hashlib.sha256(salted_input)
    
    # Return the salt and hash as a hex string
    return salt.hex() + hash_object.hexdigest()