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
        return "admin" if username == "admin" else "regular"

    def _generate_file_id(self):
        """Generate a secure random file ID"""
        return secrets.token_hex(16)

    def _hash_content(self, content):
        """Create a secure hash of file content"""
        return hashlib.sha256(content.encode()).hexdigest()

    def view_file(self, username, filename):
        """View a file's contents if user has access"""
        safe_path = Path(filename).resolve()
        if not self._is_safe_path(safe_path):
            raise ValueError("Invalid file path")
        
        file_path = self.base_directory / safe_path
        if not file_path.is_file():
            raise FileNotFoundError("File not found")
        
        access_level = self._get_user_access(username)
        if access_level == "regular" and not file_path.is_file():
            raise PermissionError("Access denied")
        
        with open(file_path, 'r') as f:
            content = f.read()
        return self._hash_content(content)

    def create_file(self, username, filename, content):
        """Create a new file with given content"""
        safe_path = Path(filename).resolve()
        if not self._is_safe_path(safe_path):
            raise ValueError("Invalid file path")
        
        file_id = self._generate_file_id()
        file_path = self.base_directory / safe_path / file_id
        
        access_level = self._get_user_access(username)
        if access_level != "admin":
            raise PermissionError("Access denied")
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_id

    def delete_file(self, username, filename):
        """Delete a file if user has access"""
        safe_path = Path(filename).resolve()
        if not self._is_safe_path(safe_path):
            raise ValueError("Invalid file path")
        
        file_path = self.base_directory / safe_path
        
        access_level = self._get_user_access(username)
        if access_level != "admin":
            raise PermissionError("Access denied")
        
        if file_path.is_file():
            os.remove(file_path)
        elif file_path.is_dir():
            shutil.rmtree(file_path)