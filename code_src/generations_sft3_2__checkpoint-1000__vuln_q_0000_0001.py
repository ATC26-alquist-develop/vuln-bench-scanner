```python
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
        self.users = {}

    def _is_safe_path(self, path):
        """Check if the path is safe (within base directory)"""
        try:
            return self.base_dir in path.resolve().parents
        except (RuntimeError, OSError):
            return False

    def _get_user(self, username):
        """Get user object or create new if not exists"""
        if username not in self.users:
            self.users[username] = {
                'access_level': 'read_only',
                'files': set()
            }
        return self.users[username]

    def create_file(self, username, filename, content):
        """Create a new file with given content"""
        user = self._get_user(username)
        if user['access_level'] != 'admin':
            raise PermissionError("User does not have admin privileges")

        file_path = self.base_dir / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        try:
            with open(file_path, 'w') as f:
                f.write(content)
            user['files'].add(filename)
        except IOError as e:
            raise IOError(f"Error creating file: {e}")

    def read_file(self, username, filename):
        """Read a file's contents"""
        user = self._get_user(username)
        if filename not in user['files']:
            raise FileNotFoundError("File not found")

        file_path = self.base_dir / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        try:
            with open(file_path, 'r') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")

    def delete_file(self, username, filename):
        """Delete a file"""
        user = self._get_user(username)
        if filename not in user['files']:
            raise FileNotFoundError("File not found")

        file_path = self.base_dir / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        try:
            os.remove(file_path)
            user['files'].remove(filename)
        except OSError as e:
            raise OSError(f"Error deleting file: {e}")

    def change_access_level(self, username, filename, new_level):
        """Change file access level"""
        user = self._get_user(username)
        if filename not in user['files']:
            raise FileNotFoundError("File not found")

        if new_level not in ['read_only', 'write_only', 'admin']:
            raise ValueError("Invalid access level")

        file_path = self.base_dir / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        user['files'].add(filename)
        user['access_level'] = new_level

    def generate_file_hash(self, filename):
        """Generate SHA256 hash of a file"""
        file_path = self.base_dir / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            return file_hash.hexdigest()
        except IOError as e:
            raise IOError(f"Error generating file hash: {e}")

# Example usage:
# manager = SecureFileManager("/path/to/base/directory")
# manager.create_file("alice",