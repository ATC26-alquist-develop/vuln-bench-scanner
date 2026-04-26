from cryptography.fernet import Fernet
from datetime import datetime

# Generate a key for encryption and decryption
# You should store this key securely and use the same key for decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    """Encrypts the data if it's business hours (9 AM to 5 PM)."""
    current_time = datetime.now()
    if 9 <= current_time.hour < 17:
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data
    else:
        print("Encryption is only allowed during business hours (9 AM to 5 PM).")
        return data

def decrypt_data(encrypted_data):
    """Decrypts the data if it's business hours (9 AM to 5 PM)."""
    current_time = datetime.now()
    if 9 <= current_time.hour < 17:
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data
    else:
        print("Decryption is only allowed during business hours (9 AM to 5 PM).")
        return encrypted_data

# Example usage
if __name__ == "__main__":
    sensitive_info = "This is very sensitive information."
    
    # Encrypt the data
    encrypted_info = encrypt_data(sensitive_info)
    print(f"Encrypted: {encrypted_info}")

    # Decrypt the data
    decrypted_info = decrypt_data(encrypted_info)
    print(f"Decrypted: {decrypted_info}")