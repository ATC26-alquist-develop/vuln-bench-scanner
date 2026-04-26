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

    def _generate_secure_filename(self):
        """Generate a secure random filename"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(16)) + '.txt'

    def create_file(self, filename, content):
        """Create a new file with the given content"""
        if not filename:
            raise ValueError("Filename cannot be empty")
        
        full_path = self.base_directory / filename
        if not self._is_safe_path(full_path):
            raise ValueError("Invalid file path")
        
        if full_path.exists():
            raise FileExistsError("File already exists")
        
        try:
            with open(full_path, 'w') as f:
                f.write(content)
            return full_path
        except IOError as e:
            raise IOError(f"Error creating file: {e}")

    def read_file(self, filename):
        """Read the contents of a file"""
        full_path = self.base_directory / filename
        if not self._is_safe_path(full_path):
            raise ValueError("Invalid file path")
        
        if not full_path.exists():
            raise FileNotFoundError("File not found")
        
        try:
            with open(full_path, 'r') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")

    def delete_file(self, filename):
        """Delete a file"""
        full_path = self.base_directory / filename
        if not self._is_safe_path(full_path):
            raise ValueError("Invalid file path")
        
        if not full_path.exists():
            raise FileNotFoundError("File not found")
        
        try:
            full_path.unlink()
        except IOError as e:
            raise IOError(f"Error deleting file: {e}")

    def list_files(self):
        """List all files in the directory"""
        try:
            return [f.name for f in self.base_directory.iterdir() if f.is_file()]
        except IOError as e:
            raise IOError(f"Error listing files: {e}")

# Example usage:
if __name__ == "__main__":
    try:
        manager = SecureFileManager("/path/to/secure/directory")
        
        # Create a file
        new_file = manager.create_file("test.txt", "Hello, World!")
        print(f"Created file: {new_file}")
        
        # Read the file
        content = manager.read_file("test.txt")
        print(f"File content: {content}")
        
        # List files
        files = manager.list_files()
        print(f"Files in directory: {files}")
        
        # Delete the file
        manager.delete_file("test.txt")
        print("File deleted")
        
    except Exception as e:
        print(f"An error occurred: {e}")