import hashlib

def hash_password(password):
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update the hash object with the bytes-like object (password)
    sha256_hash.update(password_bytes)
    
    # Get the hexadecimal representation of the hash
    hashed_password = sha256_hash.hexdigest()
    
    return hashed_password

# Example usage
password = "my_secure_password"
hashed = hash_password(password)
print(f"Original password: {password}")
print(f"Hashed password: {hashed}")