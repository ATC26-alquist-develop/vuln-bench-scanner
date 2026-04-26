import bcrypt

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def store_password(user_id, password):
    hashed_password = hash_password(password)
    # Store the hashed password in your database
    # Example: database.store_user(user_id, hashed_password)
    print(f"Stored hashed password for user {user_id}: {hashed_password}")

# Example usage
user_id = 1
password = "my_secure_password"
store_password(user_id, password)