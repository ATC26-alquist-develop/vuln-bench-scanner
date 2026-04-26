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
            self.users[username] = {'read': False, 'write': False, 'delete': False}
        return self.users[username]

    def create_file(self, username, filename, content):
        """Create a new file with specified content"""
        if not self._get_user_permissions(username)['write']:
            raise PermissionError("User does not have write permission")

        path = self.base_dir / filename
        if not self._is_safe_path(path):
            raise ValueError("Invalid file path")

        try:
            with open(path, 'w') as f:
                f.write(content)
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        except IOError as e:
            raise IOError(f"Error creating file: {e}")

    def read_file(self, username, filename):
        """Read a file's contents"""
        if not self._get_user_permissions(username)['read']:
            raise PermissionError("User does not have read permission")

        path = self.base_dir / filename
        if not self._is_safe_path(path):
            raise ValueError("Invalid file path")

        try:
            with open(path, 'r') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")

    def delete_file(self, username, filename):
        """Delete a file"""
        if not self._get_user_permissions(username)['delete']:
            raise PermissionError("User does not have delete permission")

        path = self.base_dir / filename
        if not self._is_safe_path(path):
            raise ValueError("Invalid file path")

        try:
            os.remove(path)
        except OSError as e:
            raise OSError(f"Error deleting file: {e}")

    def add_user(self, username, password):
        """Add a new user with a hashed password"""
        if username in self.users:
            raise ValueError("User already exists")
        
        salt = secrets.token_bytes(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        self.users[username] = {'salt': salt, 'hashed_password': hashed_password}

    def authenticate_user(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), user['salt'], 100000)
        return secrets.compare_digest(hashed_password, user['hashed_password'])

# Example usage:
if __name__ == "__main__":
    file_manager = SecureFileManager("/path/to/secure/directory")
    
    # Add users
    file_manager.add_user("alice", "password123")
    file_manager.add_user("bob", "securepass")
    
    # Authenticate users
    if file_manager.authenticate_user("alice", "password123"):
        print("Alice authenticated successfully")
        
        # Create a file
        file_manager.create_file("alice", "test.txt", "Hello, World!")
        
        # Read the file