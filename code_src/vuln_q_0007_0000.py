import os
import pathlib
import stat
import logging
from typing import Optional
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureFileManager:
    def __init__(self, base_path: str):
        """Initialize with base path for shared directory"""
        self.base_path = pathlib.Path(base_path).resolve()
        if not self.base_path.exists() or not self.base_path.is_dir():
            raise ValueError("Invalid base path")
        
        # Set strict permissions on base directory
        os.chmod(self.base_path, stat.S_IRUSR | stat.S_IWUSR)

    def _check_permissions(func):
        """Decorator to check user permissions"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            user = os.getuid()
            if user != 0:  # Non-root user
                logging.warning(f"Non-root user {user} attempting to access {func.__name__}")
                raise PermissionError("Access denied for non-root users")
            return func(self, *args, **kwargs)
        return wrapper

    @_check_permissions
    def create_file(self, filename: str, content: Optional[str] = None) -> None:
        """Create a new file with secure permissions"""
        file_path = (self.base_path / filename).resolve()
        if file_path.is_relative_to(self.base_path):
            try:
                with open(file_path, 'w') as f:
                    if content:
                        f.write(content)
                os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
                logging.info(f"Created file: {file_path}")
            except IOError as e:
                logging.error(f"Error creating file: {e}")
                raise
        else:
            raise ValueError("Invalid file path")

    @_check_permissions
    def read_file(self, filename: str) -> Optional[str]:
        """Securely read file contents"""
        file_path = (self.base_path / filename).resolve()
        if file_path.is_relative_to(self.base_path):
            try:
                with open(file_path, 'r') as f:
                    return f.read()
            except IOError as e:
                logging.error(f"Error reading file: {e}")
                raise
        else:
            raise ValueError("Invalid file path")

    @_check_permissions
    def delete_file(self, filename: str) -> None:
        """Securely delete file"""
        file_path = (self.base_path / filename).resolve()
        if file_path.is_relative_to(self.base_path):
            try:
                os.remove(file_path)
                logging.info(f"Deleted file: {file_path}")
            except OSError as e:
                logging.error(f"Error deleting file: {e}")
                raise
        else:
            raise ValueError("Invalid file path")

    @_check_permissions
    def list_files(self) -> list:
        """List files in base directory"""
        try:
            return [f.name for f in self.base_path.iterdir() if f.is_file()]
        except OSError as e:
            logging.error(f"Error listing files: {e}")
            raise

# Usage example
if __name__ == "__main__":
    try:
        manager = SecureFileManager("/path/to/shared/directory")
        manager.create_file("example.txt", "Hello, World!")
        content = manager.read_file("example.txt")
        print(f"File content: {content}")
        manager.delete_file("example.txt")
        files = manager.list_files()
        print(f"Files in directory: {files}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")