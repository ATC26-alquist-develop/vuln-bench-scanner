import cloudpickle
import os
import tempfile
from typing import Any

class SecureDataHandler:
    def __init__(self):
        # Use secure temporary directory for file operations
        self.temp_dir = tempfile.mkdtemp(prefix='secure_data_')
        # Maximum file size limit (e.g., 100MB)
        self.MAX_FILE_SIZE = 100 * 1024 * 1024

    def save_data(self, data: Any, filename: str) -> None:
        """Securely save data using cloudpickle."""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        if not safe_filename:
            raise ValueError("Invalid filename")
        
        # Check file size
        if len(str(data)) > self.MAX_FILE_SIZE:
            raise ValueError("Data exceeds maximum allowed size")
        
        # Use secure temporary file for writing
        temp_file = tempfile.NamedTemporaryFile(dir=self.temp_dir, delete=False)
        
        try:
            cloudpickle.dump(data, temp_file)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_file_path = temp_file.name
            
            # Rename to final filename
            os.rename(temp_file_path, os.path.join(self.temp_dir, safe_filename))
        finally:
            # Ensure temporary file is closed
            if 'temp_file' in locals():
                temp_file.close()

    def load_data(self, filename: str) -> Any:
        """Securely load data using cloudpickle."""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        if not safe_filename:
            raise ValueError("Invalid filename")
        
        file_path = os.path.join(self.temp_dir, safe_filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} not found")
        
        if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
            raise ValueError("File exceeds maximum allowed size")
        
        with open(file_path, 'rb') as file:
            return cloudpickle.load(file)

    def __del__(self):
        """Clean up temporary directory."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

# Example usage
if __name__ == "__main__":
    handler = SecureDataHandler()
    
    # Save data
    data_to_save = {"complex": [1, 2, 3], "nested": {"a": 1, "b": 2}}
    handler.save_data(data_to_save, "test_data.pkl")
    
    # Load data
    loaded_data = handler.load_data("test_data.pkl")
    print("Loaded data:", loaded_data)