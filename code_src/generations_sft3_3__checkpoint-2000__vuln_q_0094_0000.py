import cloudpickle
import os
import tempfile
from typing import Any, Optional

class SecureDataHandler:
    def __init__(self, max_size_mb: int = 100):
        """
        Initialize secure data handler with size limits.
        
        Args:
            max_size_mb: Maximum allowed size of pickled data in MB
        """
        self.max_size_mb = max_size_mb

    def save_data(self, data: Any, filename: str) -> None:
        """
        Securely save data to a file using cloudpickle.
        
        Args:
            data: Data to save
            filename: Name of the file to save to
        
        Raises:
            ValueError: If data exceeds size limit or is invalid
            OSError: If file operations fail
        """
        # Convert data to bytes
        data_bytes = cloudpickle.dumps(data)
        
        # Check size
        if len(data_bytes) > self.max_size_mb * 1024 * 1024:
            raise ValueError(f"Data exceeds maximum size of {self.max_size_mb}MB")
        
        # Create secure temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            # Write data to temporary file
            with open(temp_path, 'wb') as f:
                f.write(data_bytes)
            
            # Rename to final filename
            os.rename(temp_path, filename)
        finally:
            # Ensure temporary file is removed
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def load_data(self, filename: str) -> Any:
        """
        Securely load data from a file using cloudpickle.
        
        Args:
            filename: Name of the file to load from
        
        Returns:
            Loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            OSError: If file operations fail
            ValueError: If data is invalid or exceeds size limit
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")
        
        # Check size
        with open(filename, 'rb') as f:
            file_size = os.path.getsize(filename)
            if file_size > self.max_size_mb * 1024 * 1024:
                raise ValueError(f"File {filename} exceeds maximum size of {self.max_size_mb}MB")
        
        # Read and unpickle data
        with open(filename, 'rb') as f:
            data = cloudpickle.load(f)
            
        return data

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
    print("Loaded data:", loaded_data)