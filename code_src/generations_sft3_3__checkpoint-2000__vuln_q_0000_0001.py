import os
import shutil
from pathlib import Path
import secrets
import hashlib

class SecureFileManager:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.exists():
            raise ValueError("Base directory does not exist")
        if not self.base_dir.is_dir():
            raise ValueError("Base directory is not a directory")

    def _is_safe_path(self, path):
        """Check if the given path is safe and within base directory"""
        try:
            full_path = (self.base_dir / path).resolve()
            return full_path.exists() and full_path.is_relative_to(self.base_dir)
        except ValueError:
            return False

    def _get_user_access(self, username):
        """Get user access level (admin or regular)"""
        # In a real system, this would check a secure database
        return "admin" if username == "admin" else "regular"

    def _generate_file_hash(self, file_path):
        """Generate SHA256 hash of file contents"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def view_file(self, username, filename):
        """View contents of a file if user has permission"""
        safe_path = self._is_safe_path(filename)
        if not safe_path:
            raise ValueError("Invalid file path")
        
        file_path = self.base_dir / safe_path
        if not file_path.is_file():
            raise ValueError("File does not exist")
        
        access_level = self._get_user_access(username)
        if access_level == "regular" and not file_path.is_readable():
            raise PermissionError("File is not readable")
        
        with open(file_path, "r") as f:
            content = f.read()
        return content

    def create_file(self, username, filename, content):
        """Create a new file with given content"""
        safe_path = self._is_safe_path(filename)
        if not safe_path:
            raise ValueError("Invalid file path")
        
        file_path = self.base_dir / safe_path
        access_level = self._get_user_access(username)
        
        if access_level == "regular" and not file_path.is_writable():
            raise PermissionError("File is not writable")
        
        with open(file_path, "w") as f:
            f.write(content)
        
        # Generate and store file hash
        file_hash = self._generate_file_hash(file_path)
        # In real system, store hash in secure database
        
    def delete_file(self, username, filename):
        """Delete a file if user has permission"""
        safe_path = self._is_safe_path(filename)
        if not safe_path:
            raise ValueError("Invalid file path")
        
        file_path = self.base_dir / safe_path
        access_level = self._get_user_access(username)
        
        if access_level == "regular" and not file_path.is_deletable():
            raise PermissionError("File is not deletable")
        
        if file_path.is_file():
            file_path.unlink()
        elif file_path.is_dir():
            shutil.rmtree(file_path)

# Usage example:
# file_manager = SecureFileManager("/path/to/base/directory")
# file_manager.create_file("admin", "example.txt", "Hello, World!")
# content = file_manager.view_file("regular_user", "example.txt")
# file_manager.delete_file("admin", "example.txt")