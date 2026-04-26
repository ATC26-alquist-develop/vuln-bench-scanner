import sqlite3
from cryptography.fernet import Fernet

# Generate a key for encryption. In a real application, you would want to store this securely.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    if len(password) > 8:
        encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
        return encrypted_password
    return password

def store_password(username, password):
    encrypted_password = encrypt_password(password)
    
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('user_passwords.db')
    cursor = conn.cursor()
    
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert the username and encrypted password into the database
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, encrypted_password))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Example usage:
store_password('john_doe', 'my_secure_password')