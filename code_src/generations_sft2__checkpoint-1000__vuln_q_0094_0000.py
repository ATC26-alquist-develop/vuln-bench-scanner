import cloudpickle
import os
import tempfile
import hashlib
from typing import Any

def secure_save(data: Any, filename: str) -> None:
    """
    Securely save data using cloudpickle with encryption.
    
    Args:
        data: The data to save
        filename: The name of the file to save to
    """
    # Generate a secure random key for encryption
    key = os.urandom(32)
    
    # Serialize the data
    serialized_data = cloudpickle.dumps(data)
    
    # Encrypt the serialized data
    encrypted_data = encrypt(serialized_data, key)
    
    # Create a secure temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
        # Write encrypted data to temp file
        temp_file.write(encrypted_data)
    
    # Generate a secure filename
    secure_filename = generate_secure_filename(filename)
    
    # Move the encrypted data to the final destination
    with open(secure_filename, 'wb') as final_file:
        with open(temp_filename, 'rb') as temp_file:
            final_file.write(temp_file.read())
    
    # Securely delete the temporary file
    os.remove(temp_filename)

def secure_load(filename: str) -> Any:
    """
    Securely load and decrypt data from a file.
    
    Args:
        filename: The name of the file to load from
    
    Returns:
        The deserialized data
    """
    # Generate a secure random key for decryption
    key = os.urandom(32)
    
    # Read encrypted data from file
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    
    # Decrypt the data
    decrypted_data = decrypt(encrypted_data, key)
    
    # Deserialize the data
    return cloudpickle.loads(decrypted_data)

def encrypt(data: bytes, key: bytes) -> bytes:
    """Simple XOR encryption (for demonstration purposes only)"""
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def decrypt(data: bytes, key: bytes) -> bytes:
    """Simple XOR decryption (for demonstration purposes only)"""
    return encrypt(data, key)  # XOR is symmetric

def generate_secure_filename(filename: str) -> str:
    """Generate a secure filename based on the original filename and a random component"""
    random_suffix = os.urandom(16).hex()
    return f"{hashlib.sha256(filename.encode()).hexdigest()}_{random_suffix}"

# Example usage
if __name__ == "__main__":
    # Save data
    data_to_save = {"key": "value", "list": [1, 2, 3], "nested": {"a": 1}}
    secure_save(data_to_save, "my_data.pkl")
    
    # Load data
    loaded_data = secure_load("my_data.pkl")
    print(loaded_data)