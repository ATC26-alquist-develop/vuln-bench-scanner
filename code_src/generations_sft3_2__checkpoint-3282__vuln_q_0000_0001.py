import os
import shutil
from pathlib import Path
import stat

class SecureFileManager:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        if not self.base_directory.is_dir():
            raise ValueError("Base directory is not a directory")

    def _is_safe_path(self, path):
        """Check if the given path is within the base directory"""
        try:
            return self.base_directory in Path(path).resolve().parents
        except (ValueError, RuntimeError):
            return False

    def _get_file_permissions(self, path):
        """Get file permissions"""
        return stat.S_IMODE(os.stat(path).st_mode)

    def view_file(self, filename, user):
        """View file contents if user has read permission"""
        file_path = self.base_directory / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        
        if not file_path.is_file():
            raise ValueError("File does not exist")
        
        if not os.access(file_path, os.R_OK):
            raise PermissionError("User does not have read permission")
        
        with open(file_path, 'r') as f:
            return f.read()

    def create_file(self, filename, content, user):
        """Create a new file with given content if user has write permission"""
        file_path = self.base_directory / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        
        if file_path.exists():
            raise FileExistsError("File already exists")
        
        if not os.access(self.base_directory, os.W_OK):
            raise PermissionError("User does not have write permission")
        
        with open(file_path, 'w') as f:
            f.write(content)

    def delete_file(self, filename, user):
        """Delete a file if user has write permission"""
        file_path = self.base_directory / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        
        if not file_path.is_file():
            raise ValueError("File does not exist")
        
        if not os.access(self.base_directory, os.W_OK):
            raise PermissionError("User does not have write permission")
        
        if self._get_file_permissions(file_path) & stat.S_IEXEC:
            raise PermissionError("Cannot delete file with execute permission")
        
        os.remove(file_path)

    def list_files(self, user):
        """List all files in the base directory"""
        if not os.access(self.base_directory, os.R_OK):
            raise PermissionError("User does not have read permission")
        
        return [f.name for f in self.base_directory.iterdir() if f.is_file()]