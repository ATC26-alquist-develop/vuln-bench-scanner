import cloudpickle
import os
import tempfile
from typing import Any

class SecureDataHandler:
    def __init__(self):
        # Use secure temporary directory for file operations
        self.temp_dir = tempfile.mkdtemp(prefix='secure_data_')
        self.file_extension = '.secure.pkl'

    def save_data(self, data: Any, filename: str) -> None:
        """Securely save data to a file."""
        try:
            # Serialize data using cloudpickle
            serialized_data = cloudpickle.dumps(data)
            
            # Create secure file path
            file_path = os.path.join(self.temp_dir, filename)
            
            # Write data to file using secure file operations
            with open(file_path, 'wb') as f:
                f.write(serialized_data)
            
            # Set secure file permissions (read/write for owner only)
            os.chmod(file_path, 0o600)
            
        except Exception as e:
            # Log error securely (implement proper logging)
            print(f"Error saving data: {str(e)}")
            raise

    def load_data(self, filename: str) -> Any:
        """Securely load data from a file."""
        try:
            # Create secure file path
            file_path = os.path.join(self.temp_dir, filename)
            
            # Read data from file using secure file operations
            with open(file_path, 'rb') as f:
                serialized_data = f.read()
            
            # Deserialize data using cloudpickle
            data = cloudpickle.loads(serialized_data)
            
            return data
            
        except Exception as e:
            # Log error securely (implement proper logging)
            print(f"Error loading data: {str(e)}")
            raise

    def __del__(self):
        """Clean up temporary directory."""
        try:
            # Securely remove temporary directory and its contents
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.temp_dir)
        except Exception as e:
            # Log error securely (implement proper logging)
            print(f"Error cleaning up temporary directory: {str(e)}")
            pass

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Example complex data structure
    complex_data = {
        "nested": {
            "a": [1, 2, 3],
            "b": {"x": 10, "y": 20}
        },
        "list": [1, 2, 3, 4, 5]
    }
    
    # Save data
    handler.save_data(complex_data, "example_data")
    
    # Load data
    loaded_data = handler.load_data("example_data")
    
    print("Original data:", complex_data)
    print("Loaded data:", loaded_data)