import cloudpickle
import os
import tempfile
from typing import Any

class SecureDataHandler:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="secure_data_")
        self.max_file_size = 1024 * 1024  # 1MB limit

    def save_data(self, data: Any, filename: str) -> None:
        """Securely save data to a file using cloudpickle."""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        if not safe_filename:
            raise ValueError("Invalid filename")
        
        file_path = os.path.join(self.temp_dir, safe_filename)
        
        # Check file size
        if os.path.getsize(file_path) > self.max_file_size:
            raise ValueError("File size exceeds maximum allowed size")
        
        try:
            with open(file_path, 'wb') as f:
                cloudpickle.dump(data, f)
        except Exception as e:
            raise RuntimeError(f"Failed to save data: {str(e)}")

    def load_data(self, filename: str) -> Any:
        """Securely load data from a file using cloudpickle."""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        if not safe_filename:
            raise ValueError("Invalid filename")
        
        file_path = os.path.join(self.temp_dir, safe_filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} not found")
        
        try:
            with open(file_path, 'rb') as f:
                return cloudpickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load data: {str(e)}")

    def __del__(self):
        """Clean up temporary directory on object destruction."""
        try:
            os.rmdir(self.temp_dir)
        except OSError:
            pass  # Ignore errors during cleanup

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Save data
    data_to_save = {"complex": [1, 2, 3], "nested": {"a": 1, "b": 2}}
    handler.save_data(data_to_save, "test_data.pkl")
    
    # Load data
    loaded_data = handler.load_data("test_data.pkl")
    print("Loaded data:", loaded_data)