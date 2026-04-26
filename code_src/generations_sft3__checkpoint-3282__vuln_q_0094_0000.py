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
        """Securely save data to a file using cloudpickle."""
        try:
            # Validate filename to prevent path traversal
            if not self._is_safe_filename(filename):
                raise ValueError("Invalid filename")

            # Create full file path
            file_path = os.path.join(self.temp_dir, filename + self.file_extension)
            
            # Serialize data
            with open(file_path, 'wb') as f:
                cloudpickle.dump(data, f)
        except Exception as e:
            raise RuntimeError(f"Error saving data: {str(e)}")

    def load_data(self, filename: str) -> Any:
        """Securely load data from a file using cloudpickle."""
        try:
            # Validate filename to prevent path traversal
            if not self._is_safe_filename(filename):
                raise ValueError("Invalid filename")

            # Create full file path
            file_path = os.path.join(self.temp_dir, filename + self.file_extension)
            
            # Load data
            with open(file_path, 'rb') as f:
                return cloudpickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Error loading data: {str(e)}")

    def _is_safe_filename(self, filename: str) -> bool:
        """Validate filename to prevent path traversal."""
        return not os.path.isabs(filename) and '..' not in filename.split(os.sep)

    def cleanup(self) -> None:
        """Securely clean up temporary directory."""
        try:
            # Remove all files in the temporary directory
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                os.remove(file_path)
            os.rmdir(self.temp_dir)
        except Exception as e:
            # Log error but don't expose details to user
            print(f"Error during cleanup: {str(e)}")

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
    handler.save_data(data, "example_data")
    
    # Load data
    loaded_data = handler.load_data("example_data")
    print("Loaded data:", loaded_data)
    
    # Cleanup
    handler.cleanup()