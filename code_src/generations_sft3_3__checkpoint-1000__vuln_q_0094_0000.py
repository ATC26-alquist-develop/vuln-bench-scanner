import cloudpickle
import os
import tempfile
import hashlib
from typing import Any, Dict

class SecureDataHandler:
    def __init__(self, max_size_mb: int = 10):
        self.max_size_mb = max_size_mb

    def save_data(self, data: Any, filename: str) -> None:
        """Securely save data to a file using cloudpickle."""
        if not isinstance(data, (dict, list, tuple, str, int, float, bool, type(None))):
            raise ValueError("Unsupported data type")
        
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        if not filename.endswith('.pkl'):
            filename += '.pkl'
        
        if not os.path.dirname(filename):
            raise ValueError("Filename must contain directory path")
        
        try:
            # Serialize data
            serialized_data = cloudpickle.dumps(data)
            
            # Calculate file size
            file_size_mb = len(serialized_data) / (1024 * 1024)
            
            if file_size_mb > self.max_size_mb:
                raise ValueError(f"Data exceeds maximum allowed size of {self.max_size_mb}MB")
            
            # Create secure temporary file
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                temp_file.write(serialized_data)
                temp_file_path = temp_file.name
            
            # Generate secure filename
            secure_filename = self._generate_secure_filename(filename)
            
            # Move temporary file to final location
            os.replace(temp_file_path, secure_filename)
            
        except Exception as e:
            raise RuntimeError(f"Error saving data: {str(e)}")

    def load_data(self, filename: str) -> Any:
        """Securely load data from a file using cloudpickle."""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        if not filename.endswith('.pkl'):
            raise ValueError("Filename must end with .pkl")
        
        try:
            with open(filename, 'rb') as file:
                serialized_data = file.read()
            
            # Calculate file size
            file_size_mb = len(serialized_data) / (1024 * 1024)
            
            if file_size_mb > self.max_size_mb:
                raise ValueError(f"Data exceeds maximum allowed size of {self.max_size_mb}MB")
            
            # Deserialize data
            return cloudpickle.loads(serialized_data)
        
        except Exception as e:
            raise RuntimeError(f"Error loading data: {str(e)}")

    def _generate_secure_filename(self, filename: str) -> str:
        """Generate a secure filename to prevent path traversal attacks."""
        # Remove any directory components and replace with a unique identifier
        base_name = os.path.basename(filename)
        return f"{base_name}_{hashlib.sha256(os.urandom(32)).hexdigest()[:16]}.pkl"

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Example data
    data = {
        "name": "John Doe",
        "age": 30,
        "scores": [85, 90, 78],
        "is_active": True
    }
    
    # Save data
    try:
        handler.save_data(data, "secure_data.pkl")
        print("Data saved successfully")
    except Exception as e:
        print(f"Error saving data: {str(e)}")
    
    # Load data
    try:
        loaded_data = handler.load_data("secure_data.pkl")
        print("Data loaded successfully")
        print(loaded_data)
    except Exception as e:
        print(f"Error loading data: {str(e)}")