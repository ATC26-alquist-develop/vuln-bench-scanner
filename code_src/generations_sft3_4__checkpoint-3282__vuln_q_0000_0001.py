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
            
        if user not in ['admin', 'user']:
            raise PermissionError("User does not have access")
            
        if user == 'admin' and self._get_file_permissions(file_path) & stat.S_IWOTH:
            raise PermissionError("File has world write permission")
            
        if user == 'user' and self._get_file_permissions(file_path) & stat.S_IRWXO:
            raise PermissionError("File has excessive permissions")
            
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except PermissionError:
            raise PermissionError("Permission denied to view file")

    def create_file(self, filename, content, user):
        """Create a new file with given content if user has write permission"""
        file_path = self.base_directory / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
            
        if user not in ['admin', 'user']:
            raise PermissionError("User does not have access")
            
        if user == 'admin' and self._get_file_permissions(file_path) & stat.S_IWOTH:
            raise PermissionError("File has world write permission")
            
        if user == 'user' and self._get_file_permissions(file_path) & stat.S_IRWXO:
            raise PermissionError("File has excessive permissions")
            
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
        except PermissionError:
            raise PermissionError("Permission denied to create file")

    def delete_file(self, filename, user):
        """Delete a file if user has write permission"""
        file_path = self.base_directory / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
            
        if user not in ['admin', 'user']:
            raise PermissionError("User does not have access")
            
        if user == 'admin' and self._get_file_permissions(file_path) & stat.S_IWOTH:
            raise PermissionError("File has world write permission")
            
        if user == 'user' and self._get_file_permissions(file_path) & stat.S_IRWXO:
            raise PermissionError("File has excessive permissions")
            
        try:
            os.remove(file_path)
        except PermissionError:
            raise PermissionError("Permission denied to delete file")