import bcrypt
from cryptography.fernet import Fernet
import os

# Generate a key for AES encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt a password using AES
def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

# Store the password in the database
def store_password_in_database(username, password):
    # Check if the password is longer than 8 characters
    if len(password) > 8:
        # Encrypt the password
        key = generate_key()
        encrypted_password = encrypt_password(password, key)
        # Store the username and encrypted password in the database
        # This is a placeholder for the actual database storage logic
        print(f"Storing password for {username} with key: {key.hex()}")
    else:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        # Store the username and hashed password in the database
        # This is a placeholder for the actual database storage logic
        print(f"Storing password for {username} with bcrypt hash")

# Example usage
store_password_in_database("user123", "securepassword123")
store_password_in_database("user456", "shortpassword")