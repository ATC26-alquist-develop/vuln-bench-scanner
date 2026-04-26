```python
import os
import stat
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
            return self.base_dir.resolve() in Path(path).resolve().parents
        except (ValueError, RuntimeError):
            return False

    def _get_user_permissions(self, username):
        """Get user permissions based on access level"""
        if username not in self.users:
            raise ValueError("User not found")
        return self.users[username]

    def create_file(self, username, filename, content):
        """Create a new file with given content"""
        permissions = self._get_user_permissions(username)
        if not permissions['can_write']:
            raise PermissionError("User does not have write permission")

        file_path = (self.base_dir / filename).resolve()
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        if file_path.exists():
            raise FileExistsError("File already exists")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
        return file_path

    def read_file(self, username, filename):
        """Read a file's contents"""
        permissions = self._get_user_permissions(username)
        if not permissions['can_read']:
            raise PermissionError("User does not have read permission")

        file_path = (self.base_dir / filename).resolve()
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def delete_file(self, username, filename):
        """Delete a file"""
        permissions = self._get_user_permissions(username)
        if not permissions['can_delete']:
            raise PermissionError("User does not have delete permission")

        file_path = (self.base_dir / filename).resolve()
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")

        if not file_path.exists():
            raise FileNotFoundError("File not found")

        os.remove(file_path)
        return True

    def add_user(self, username, password, access_level):
        """Add a new user with specified access level"""
        if username in self.users:
            raise ValueError("User already exists")
        if not isinstance(access_level, dict) or 'can_write' not in access_level or 'can_read' not in access_level or 'can_delete' not in access_level:
            raise ValueError("Invalid access level")
        
        salt = secrets.token_bytes(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        self.users[username] = {
            'password': hashed_password,
            'salt': salt,
            'access_level': access_level
        }

    def authenticate_user(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False
        user = self.users[username]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), user['salt'], 100000)
        return secrets.compare_digest(hashed_password, user['password'])

# Example usage:
if __name__ == "__main__":
    file_manager = SecureFileManager("/path/to/base/directory")
    
    # Add users