import os
import shutil
from pathlib import Path
import logging
from typing import List, Optional

class SecureFileManager:
    def __init__(self, base_path: str):
        """Initialize the file manager with a base path."""
        self.base_path = Path(base_path).resolve()
        if not self.base_path.exists():
            raise ValueError("Base path does not exist")
        self.logger = logging.getLogger(__name__)

    def _sanitize_path(self, path: str) -> Path:
        """Sanitize and resolve the given path."""
        full_path = (self.base_path / path).resolve()
        if not full_path.is_relative_to(self.base_path):
            raise ValueError("Access denied: Path outside base directory")
        return full_path

    def list_files(self, user_path: str) -> List[str]:
        """List files in the specified directory."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Not a directory")
            return [f.name for f in path.iterdir() if f.is_file()]
        except (ValueError, OSError) as e:
            self.logger.error(f"Error listing files: {str(e)}")
            raise

    def create_file(self, user_path: str, filename: str, content: Optional[str] = None) -> None:
        """Create a new file with optional content."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Not a directory")
            file_path = path / filename
            if file_path.exists():
                raise ValueError("File already exists")
            if content:
                file_path.write_text(content)
            else:
                file_path.touch()
        except (ValueError, OSError) as e:
            self.logger.error(f"Error creating file: {str(e)}")
            raise

    def delete_file(self, user_path: str, filename: str) -> None:
        """Delete a file."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Not a directory")
            file_path = path / filename
            if not file_path.is_file():
                raise ValueError("File does not exist")
            file_path.unlink()
        except (ValueError, OSError) as e:
            self.logger.error(f"Error deleting file: {str(e)}")
            raise

    def read_file(self, user_path: str, filename: str) -> str:
        """Read the contents of a file."""
        try:
            path = self._sanitize_path(user_path)
            if not path.is_dir():
                raise ValueError("Not a directory")
            file_path = path / filename
            if not file_path.is_file():
                raise ValueError("File does not exist")
            return file_path.read_text()
        except (ValueError, OSError) as e:
            self.logger.error(f"Error reading file: {str(e)}")
            raise

def main():
    logging.basicConfig(level=logging.INFO)
    base_path = "/path/to/secure/directory"
    file_manager = SecureFileManager(base_path)

    try:
        # Example usage
        files = file_manager.list_files("documents")
        print("Files in documents:", files)

        file_manager.create_file("documents", "new_file.txt", "Hello, World!")
        content = file_manager.read_file("documents", "new_file.txt")
        print("File content:", content)

        file_manager.delete_file("documents", "new_file.txt")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()