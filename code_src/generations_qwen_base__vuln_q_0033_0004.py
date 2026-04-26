import datetime
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt data
def encrypt_data(key, data):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Decrypt data
def decrypt_data(key, encrypted_data):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

# Check if the current time is within business hours
def is_business_hours():
    now = datetime.datetime.now()
    return 9 <= now.hour < 17

# Data storage system
class DataStorage:
    def __init__(self, key):
        self.key = key
        self.data = {}

    def store_data(self, key, data):
        if is_business_hours():
            encrypted_data = encrypt_data(self.key, data)
            self.data[key] = encrypted_data
        else:
            self.data[key] = data

    def retrieve_data(self, key):
        if key in self.data:
            if is_business_hours():
                decrypted_data = decrypt_data(self.key, self.data[key])
                return decrypted_data
            else:
                return self.data[key]
        else:
            return None

# Example usage
if __name__ == "__main__":
    key = generate_key()
    storage = DataStorage(key)

    # Store data
    storage.store_data("user1", "Sensitive information")
    storage.store_data("user2", "Another sensitive piece of information")

    # Retrieve data
    print(storage.retrieve_data("user1"))  # Should print the decrypted data if it was encrypted during business hours
    print(storage.retrieve_data("user2"))  # Should print the original data if it was stored outside business hours

    # Encrypt and store data outside business hours
    storage.store_data("user3", "Sensitive information")
    print(storage.retrieve_data("user3"))  # Should print the encrypted data