```python
import os
import stat
from pathlib import Path
import secrets
import hashlib

class SecureFileManager:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.exists():
            raise ValueError("Base directory does not exist")
        self.users = {}

    def _is_safe_path(self, path):
        """Check if the path is safe (within base directory)"""
        try:
            return self.base_directory in Path(path).resolve().parents
        except (ValueError, RuntimeError):
            return False

    def _get_user_permissions(self, username):
        """Get user permissions for a given username"""
        if username not in self.users:
            raise ValueError("User does not exist")
        return self.users[username]

    def create_file(self, username, filename, content):
        """Create a new file with the given content"""
        if not self._is_safe_path(filename):
            raise ValueError("Invalid file path")
        
        user_permissions = self._get_user_permissions(username)
        if not user_permissions['can_write']:
            raise PermissionError("User does not have write permissions")

        file_path = self.base_directory / filename
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
        except IOError as e:
            raise IOError(f"Error creating file: {e}")

    def read_file(self, username, filename):
        """Read the contents of a file"""
        if not self._is_safe_path(filename):
            raise ValueError("Invalid file path")
        
        user_permissions = self._get_user_permissions(username)
        if not user_permissions['can_read']:
            raise PermissionError("User does not have read permissions")

        file_path = self.base_directory / filename
        if not self._is_safe_path(file_path):
            raise ValueError("File not found")

        try:
            with open(file_path, 'r') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")

    def delete_file(self, username, filename):
        """Delete a file"""
        if not self._is_safe_path(filename):
            raise ValueError("Invalid file path")
        
        user_permissions = self._get_user_permissions(username)
        if not user_permissions['can_delete']:
            raise PermissionError("User does not have delete permissions")

        file_path = self.base_directory / filename
        if not self._is_safe_path(file_path):
            raise ValueError("File not found")

        try:
            os.remove(file_path)
        except OSError as e:
            raise OSError(f"Error deleting file: {e}")

    def add_user(self, username, password, permissions):
        """Add a new user with specified permissions"""
        if username in self.users:
            raise ValueError("User already exists")
        
        if not isinstance(permissions, dict) or 'can_write' not in permissions or 'can_read' not in permissions or 'can_delete' not in permissions:
            raise ValueError("Invalid permissions")

        salt = secrets.token_bytes(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        self.users[username] = {
            'password': hashed_password,
            'salt': salt,
            'permissions': permissions
        }

    def authenticate_user(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), user['salt'], 100000)
        return secrets.compare_digest(hashed_password, user['password'])

# Example usage:
if __name__