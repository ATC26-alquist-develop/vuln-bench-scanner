import hashlib

def hash_password(password):
    # Create a sha256 hash object
    sha_signature = hashlib.sha256()
    
    # Update the hash object with the bytes of the password
    sha_signature.update(password.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return sha_signature.hexdigest()

# Example usage
password = "my_secure_password"
hashed_password = hash_password(password)
print(f"Hashed Password: {hashed_password}")

# ===== cell separator =====

def verify_password(stored_hash, password):
    return stored_hash == hash_password(password)

# Example usage
stored_hash = hash_password("my_secure_password")
entered_password = "my_secure_password"
is_correct = verify_password(stored_hash, entered_password)
print(f"Is the password correct? {is_correct}")