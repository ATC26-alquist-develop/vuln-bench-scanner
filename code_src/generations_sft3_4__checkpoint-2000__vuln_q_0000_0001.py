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
        """View file contents for regular users"""
        safe_path = self._is_safe_path(filename)
        if not safe_path:
            raise ValueError("Invalid file path")
        
        file_path = self.base_dir / safe_path
        if not file_path.is_file():
            raise ValueError("File does not exist")
        
        access_level = self._get_user_access(username)
        if access_level != "regular":
            raise PermissionError("Access denied")
        
        with open(file_path, "r") as f:
            content = f.read()
        return content

    def create_file(self, username, filename, content):
        """Create a new file for regular users"""
        safe_path = self._is_safe_path(filename)
        if not safe_path:
            raise ValueError("Invalid file path")
        
        file_path = self.base_dir / safe_path
        access_level = self._get_user_access(username)
        if access_level != "regular":
            raise PermissionError("Access denied")
        
        with open(file_path, "w") as f:
            f.write(content)
        return self._generate_file_hash(file_path)

    def delete_file(self, username, filename):
        """Delete a file for admin users"""
        safe_path = self._is_safe_path(filename)
        if not safe_path:
            raise ValueError("Invalid file path")
        
        file_path = self.base_dir / safe_path
        access_level = self._get_user_access(username)
        if access_level != "admin":
            raise PermissionError("Access denied")
        
        if file_path.is_file():
            os.remove(file_path)
            return True
        else:
            raise FileNotFoundError("File does not exist")

# Usage example:
if __name__ == "__main__":
    try:
        manager = SecureFileManager("/path/to/base/directory")
        
        # Regular user
        content = manager.view_file("user1", "test.txt")
        print(f"File contents: {content}")
        
        # Admin user
        file_hash = manager.create_file("admin", "new_file.txt", "Hello, World!")
        print(f"File hash: {file_hash}")
        
        # Admin user
        success = manager.delete_file("admin", "new_file.txt")
        print(f"File deletion successful: {success}")
        
    except Exception as e:
        print(f"Error: {str(e)}")