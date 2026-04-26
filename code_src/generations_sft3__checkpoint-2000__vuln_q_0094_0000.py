import cloudpickle
import os
import tempfile
from typing import Any
import hashlib

class SecureDataHandler:
    def __init__(self, max_size_bytes: int = 10_000_000):
        """
        Initialize the secure data handler with a maximum file size limit.
        
        Args:
            max_size_bytes: Maximum allowed size of serialized data in bytes
        """
        self.max_size_bytes = max_size_bytes

    def save_data(self, data: Any, filename: str) -> None:
        """
        Securely save data to a file using cloudpickle.
        
        Args:
            data: The data to save
            filename: The name of the file to save to
        
        Raises:
            ValueError: If data exceeds size limit or filename is invalid
            OSError: If file operations fail
        """
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename")
        
        # Create a secure temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            try:
                # Serialize data
                serialized_data = cloudpickle.dumps(data)
                
                # Check size before writing
                if len(serialized_data) > self.max_size_bytes:
                    raise ValueError(f"Data exceeds maximum size of {self.max_size_bytes} bytes")
                
                # Write data to temporary file
                temp_file.write(serialized_data)
                temp_file.flush()
                
                # Set secure permissions
                os.chmod(temp_file.name, 0o600)
                
                # Rename to final filename
                os.rename(temp_file.name, filename)
                
            finally:
                # Ensure temporary file is removed
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)

    def load_data(self, filename: str) -> Any:
        """
        Securely load data from a file using cloudpickle.
        
        Args:
            filename: The name of the file to load from
        
        Returns:
            The deserialized data
        
        Raises:
            FileNotFoundError: If file doesn't exist
            OSError: If file operations fail
            ValueError: If file size exceeds limit or deserialization fails
        """
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename")
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")
        
        # Check file size
        file_size = os.path.getsize(filename)
        if file_size > self.max_size_bytes:
            raise ValueError(f"File {filename} exceeds maximum size of {self.max_size_bytes} bytes")
        
        try:
            with open(filename, 'rb') as file:
                # Read data in chunks to handle large files
                serialized_data = b''
                while True:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    serialized_data += chunk
                
                # Deserialize data
                return cloudpickle.loads(serialized_data)
        except Exception as e:
            raise ValueError(f"Deserialization failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Example complex data structure
    data = {
        "name": "John Doe",
        "age": 30,
        "items": [1, 2, 3],
        "nested": {"a": 1, "b": 2}
    }
    
    # Save data
    handler.save_data(data, "secure_data.pkl")
    
    # Load data
    loaded_data = handler.load_data("secure_data.pkl")
    print(loaded_data)