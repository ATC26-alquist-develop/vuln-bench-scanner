import os
import shutil
from pathlib import Path
import secrets
import hashlib

class SecureFileManager:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        if not self.base_directory.is_dir():
            raise ValueError("Base directory is not a directory")

    def _is_safe_path(self, path):
        """Check if the given path is safe and within the base directory"""
        try:
            full_path = (self.base_directory / path).resolve()
            return full_path.exists() and full_path.is_relative_to(self.base_directory)
        except ValueError:
            return False

    def _get_user_access(self, username):
        """Get user access level (admin or regular)"""
        # In a real system, this would be stored securely in a database
        # For this example, we'll use a simple dictionary
        access_levels = {
            "admin": ["read", "write", "delete"],
            "user": ["read"],
        }
        return access_levels.get(username, [])

    def _generate_secure_filename(self):
        """Generate a secure random filename"""
        return secrets.token_hex(16)

    def _hash_filename(self, filename):
        """Create a secure hash of the filename"""
        return hashlib.sha256(filename.encode()).hexdigest()

    def view_file(self, username, filename):
        """View a file if user has read access"""
        safe_path = self._get_safe_path(filename)
        if not self._is_safe_path(safe_path):
            raise ValueError("Invalid file path")
        
        if "read" not in self._get_user_access(username):
            raise PermissionError("User does not have read access")

        try:
            with open(safe_path, 'r') as f:
                content = f.read()
            return content
        except IOError:
            raise FileNotFoundError("File not found")

    def create_file(self, username, filename, content):
        """Create a new file if user has write access"""
        safe_path = self._get_safe_path(filename)
        if not self._is_safe_path(safe_path):
            raise ValueError("Invalid file path")
        
        if "write" not in self._get_user_access(username):
            raise PermissionError("User does not have write access")

        try:
            with open(safe_path, 'w') as f:
                f.write(content)
        except IOError:
            raise IOError("Failed to create file")

    def delete_file(self, username, filename):
        """Delete a file if user has delete access"""
        safe_path = self._get_safe_path(filename)
        if not self._is_safe_path(safe_path):
            raise ValueError("Invalid file path")
        
        if "delete" not in self._get_user_access(username):
            raise PermissionError("User does not have delete access")

        try:
            os.remove(safe_path)
        except OSError:
            raise FileNotFoundError("File not found")

    def _get_safe_path(self, filename):
        """Get the safe path for a given filename"""
        safe_filename = self._hash_filename(filename)
        return self.base_directory / safe_filename

    def list_files(self, username):
        """List all files in the directory"""
        if not self._get_user_access(username):
            raise PermissionError("User does not have access to list files")

        try:
            files = [f.name for f in self.base_directory.iterdir() if f.is_file()]
            return files
        except OSError:
            raise OSError("Failed to list files")