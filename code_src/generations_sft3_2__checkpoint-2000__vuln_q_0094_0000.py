import cloudpickle
import os
import tempfile
import hashlib
from typing import Any

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
            ValueError: If data exceeds size limit or is corrupted
        """
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename")
        
        try:
            with open(filename, 'rb') as file:
                # Read data
                serialized_data = file.read()
                
                # Check size
                if len(serialized_data) > self.max_size_bytes:
                    raise ValueError(f"Data exceeds maximum size of {self.max_size_bytes} bytes")
                
                # Deserialize data
                return cloudpickle.loads(serialized_data)
                
        except cloudpickle.pickle.UnpicklingError:
            raise ValueError("Corrupt or malicious data detected")
        except Exception as e:
            raise OSError(f"Error loading data: {str(e)}")

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Example data
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