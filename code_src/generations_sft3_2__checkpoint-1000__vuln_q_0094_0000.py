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
        
        if len(str(data)) > self.max_size_mb * 1024 * 1024:
            raise ValueError(f"Data exceeds maximum size of {self.max_size_mb}MB")
        
        try:
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                cloudpickle.dump(data, temp_file)
            
            # Generate a secure filename
            secure_filename = self._generate_secure_filename(filename)
            
            # Move the temporary file to the final location
            os.replace(temp_file.name, secure_filename)
            
            # Set secure permissions
            os.chmod(secure_filename, 0o600)
            
        except Exception as e:
            raise RuntimeError(f"Error saving data: {str(e)}")

    def load_data(self, filename: str) -> Any:
        """Securely load data from a file using cloudpickle."""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        if not filename.endswith('.pkl'):
            raise ValueError("Filename must have .pkl extension")
        
        try:
            with tempfile.NamedTemporaryFile(mode='rb', delete=False) as temp_file:
                with open(filename, 'rb') as f:
                    data = cloudpickle.load(f)
            
            # Verify data integrity
            if not self._verify_data_integrity(data):
                raise ValueError("Data integrity check failed")
            
            return data
        
        except Exception as e:
            raise RuntimeError(f"Error loading data: {str(e)}")

    def _generate_secure_filename(self, original_filename: str) -> str:
        """Generate a secure filename to prevent path traversal attacks."""
        # Remove any potentially dangerous characters
        safe_filename = ''.join(c for c in original_filename if c.isalnum() or c in '._-')
        
        # Add a timestamp to prevent overwriting
        timestamp = str(int(time.time()))
        return f"{safe_filename}_{timestamp}.pkl"

    def _verify_data_integrity(self, data: Any) -> bool:
        """Verify the integrity of the loaded data."""
        # Implement your data integrity verification logic here
        # This is a placeholder and should be replaced with actual verification
        return True

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Save data
    data = {
        "name": "John Doe",
        "age": 30,
        "scores": [85, 90, 78],
        "is_active": True
    }
    handler.save_data(data, "user_data.pkl")
    
    # Load data
    loaded_data = handler.load_data("user_data.pkl")
    print(loaded_data)