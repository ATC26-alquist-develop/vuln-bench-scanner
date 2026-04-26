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
            # Save data using cloudpickle
            cloudpickle.dump(data, temp_file)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            
            # Set secure permissions (readable/writable only by owner)
            os.chmod(temp_file.name, 0o600)
            
            # Rename to final filename
            os.rename(temp_file.name, os.path.join(self.temp_dir, safe_filename))
        finally:
            # Ensure temporary file is removed
            temp_file.close()
            os.unlink(temp_file.name)

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
        
        # Check file size
        if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
            raise ValueError("File exceeds maximum allowed size")
        
        try:
            with open(file_path, 'rb') as f:
                return cloudpickle.load(f)
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")

    def __del__(self):
        """Clean up temporary directory on object destruction."""
        try:
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for name in files:
                    os.unlink(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.temp_dir)
        except Exception:
            pass  # Ignore cleanup errors