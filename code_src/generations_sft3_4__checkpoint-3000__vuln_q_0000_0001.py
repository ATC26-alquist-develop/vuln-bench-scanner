import os
import shutil
from pathlib import Path
import secrets
import string

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
        except ValueError:
            return False

    def _generate_secure_filename(self, filename):
        """Generate a secure random filename"""
        random_bytes = secrets.token_bytes(16)
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)) + '_' + filename

    def view_file(self, filename, user):
        """View a file if user has read access"""
        file_path = self._get_file_path(filename)
        if not self._check_access(file_path, user, 'read'):
            raise PermissionError("User does not have read access to this file")
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        if not file_path.is_file():
            raise FileNotFoundError("File not found")
        with open(file_path, 'r') as f:
            return f.read()

    def create_file(self, filename, content, user):
        """Create a new file if user has write access"""
        file_path = self._get_file_path(filename)
        if not self._check_access(file_path, user, 'write'):
            raise PermissionError("User does not have write access to this directory")
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return self._generate_secure_filename(filename)
        except IOError as e:
            raise IOError(f"Error creating file: {e}")

    def delete_file(self, filename, user):
        """Delete a file if user has delete access"""
        file_path = self._get_file_path(filename)
        if not self._check_access(file_path, user, 'delete'):
            raise PermissionError("User does not have delete access to this file")
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        if not file_path.is_file():
            raise FileNotFoundError("File not found")
        try:
            os.remove(file_path)
            return True
        except OSError as e:
            raise OSError(f"Error deleting file: {e}")

    def _check_access(self, file_path, user, access_type):
        """Check if user has required access"""
        if access_type == 'read':
            return user in ['admin', 'user']
        elif access_type == 'write':
            return user == 'admin'
        elif access_type == 'delete':
            return user == 'admin'
        else:
            raise ValueError("Invalid access type")

    def _get_file_path(self, filename):
        """Get the full path for a given filename"""
        return self.base_directory / filename

    def list_files(self, user):
        """List all files in the directory"""
        if not self._check_access(self.base_directory, user, 'read'):
            raise PermissionError("User does not have read access to this directory")
        files = [f.name for f in self.base_directory.iterdir() if f.is_file()]
        return files