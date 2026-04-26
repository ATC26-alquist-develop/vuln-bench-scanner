import hashlib

def hash_input(input_string):
    # Choose a hashing algorithm. For example, sha256
    hash_algorithm = hashlib.sha256
    # Create a new hash object
    hash_object = hash_algorithm()
    # Update the hash object with the input string
    hash_object.update(input_string.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hashed_value = hash_object.hexdigest()
    return hashed_value

# Example usage
user_input = "example_input"
hashed_input = hash_input(user_input)
print(f"Hashed Input: {hashed_input}")

# ===== cell separator =====

def verify_input(input_string, stored_hash):
    # Hash the input string
    new_hash = hash_input(input_string)
    # Compare the new hash with the stored hash
    return new_hash == stored_hash

# Example usage
user_input = "example_input"
stored_hash = 'your_stored_hash_here'
is_valid = verify_input(user_input, stored_hash)
print(f"Is valid: {is_valid}")