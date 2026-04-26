import cloudpickle
import os
import tempfile
from typing import Any
import hashlib

class SecureDataHandler:
    def __init__(self, max_size_mb: int = 100):
        """
        Initialize the secure data handler with a maximum file size limit.
        
        :param max_size_mb: Maximum allowed size in MB
        """
        self.max_size_mb = max_size_mb

    def save_data(self, data: Any, filename: str) -> None:
        """
        Securely save data to a file using cloudpickle.
        
        :param data: Data to be saved
        :param filename: Name of the file to save to
        """
        # Validate input
        if not isinstance(data, (bytes, bytearray, list, dict, str, int, float, bool)):
            raise ValueError("Unsupported data type")
        
        # Check file size
        if len(str(data)) > self.max_size_mb * 1024 * 1024:
            raise ValueError(f"Data exceeds maximum size of {self.max_size_mb}MB")

        # Create secure temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            try:
                # Serialize data
                cloudpickle.dump(data, temp_file)
                
                # Generate secure filename
                secure_filename = self._generate_secure_filename(filename)
                
                # Move temporary file to final location
                os.replace(temp_file.name, secure_filename)
            finally:
                # Ensure temporary file is removed
                os.unlink(temp_file.name)

    def load_data(self, filename: str) -> Any:
        """
        Securely load data from a file using cloudpickle.
        
        :param filename: Name of the file to load from
        :return: Loaded data
        """
        # Validate input
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")

        # Check file size
        if os.path.getsize(filename) > self.max_size_mb * 1024 * 1024:
            raise ValueError(f"File exceeds maximum size of {self.max_size_mb}MB")

        try:
            with open(filename, 'rb') as file:
                # Deserialize data
                return cloudpickle.load(file)
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")

    def _generate_secure_filename(self, original_filename: str) -> str:
        """
        Generate a secure filename by hashing the original name.
        
        :param original_filename: Original filename
        :return: Secure filename
        """
        # Create hash of filename
        filename_hash = hashlib.sha256(original_filename.encode()).hexdigest()
        
        # Append extension if it doesn't exist
        _, ext = os.path.splitext(original_filename)
        return f"{filename_hash}{ext}"

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Save data
    data_to_save = {"key": "value", "numbers": [1, 2, 3], "nested": {"a": 1, "b": 2}}
    handler.save_data(data_to_save, "secure_data.pkl")
    
    # Load data
    loaded_data = handler.load_data("secure_data.pkl")
    print(loaded_data)