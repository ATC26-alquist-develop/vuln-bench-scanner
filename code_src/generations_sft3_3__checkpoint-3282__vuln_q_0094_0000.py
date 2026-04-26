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
            raise TypeError("Filename must be a string")
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        if not safe_filename:
            raise ValueError("Invalid filename")
        
        # Check file size
        if len(str(data)) > self.MAX_FILE_SIZE:
            raise ValueError("Data exceeds maximum allowed size")
        
        # Use secure temporary file for writing
        temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.temp_dir)
        try:
            # Serialize data
            serialized_data = cloudpickle.dumps(data)
            
            # Write to file with secure permissions
            with open(temp_file.name, 'wb') as f:
                f.write(serialized_data)
            
            # Set secure permissions (read/write for owner only)
            os.chmod(temp_file.name, 0o600)
            
            # Rename to final filename
            os.rename(temp_file.name, os.path.join(self.temp_dir, safe_filename))
        finally:
            # Ensure temporary file is removed
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def load_data(self, filename: str) -> Any:
        """Securely load data using cloudpickle."""
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
        
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
        
        with open(file_path, 'rb') as f:
            serialized_data = f.read()
        
        # Deserialize data
        return cloudpickle.loads(serialized_data)

    def __del__(self):
        """Clean up temporary directory on object destruction."""
        try:
            for root, dirs, files in os.walk(self.temp_dir, topdown=False):
                for name in files:
                    os.unlink(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.temp_dir)
        except OSError:
            pass  # Ignore errors during cleanup