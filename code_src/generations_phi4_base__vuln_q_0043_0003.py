import bcrypt

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(hashed_password, password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Example usage
password = "my_secure_password"
hashed_password = hash_password(password)

# Store hashed_password in the database

# Later, when verifying the password
is_valid = check_password(hashed_password, "my_secure_password")
print(is_valid)  # Output: True