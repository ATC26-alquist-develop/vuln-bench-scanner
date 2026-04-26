import hashlib

def hash_input(user_input):
    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()
    
    # Encode the user input to bytes, then update the hash object with the bytes
    sha256_hash.update(user_input.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

# Example usage
user_input = input("Enter some text to hash: ")
hashed_value = hash_input(user_input)
print(f"Hashed value: {hashed_value}")