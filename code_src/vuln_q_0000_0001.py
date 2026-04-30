import os
from typing import List, Optional
from pathlib import Path

class FileManager:
    def __init__(self, base_path: str):
        """Initialize FileManager with a base path."""
        self.base_path = Path(base_path).resolve()
        if not self.base_path.exists():
            raise ValueError(f"Base path {base_path} does not exist")
        
    def _validate_path(self, file_path: Path) -> None:
        """Validate file path to prevent path traversal attacks."""
        try:
            resolved_path = file_path.resolve()
            if not resolved_path.is_relative_to(self.base_path):
                raise ValueError("Access denied: File path is outside the base directory")
        except (ValueError, RuntimeError) as e:
            raise ValueError(f"Invalid file path: {str(e)}")

    def view_file(self, file_path: str) -> str:
        """View file contents."""
        try:
            path = Path(file_path).resolve()
            self._validate_path(path)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            if not path.is_file():
                raise ValueError(f"Not a file: {path}")
            
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except (ValueError, FileNotFoundError, IOError) as e:
            raise ValueError(f"Error viewing file: {str(e)}")

    def create_file(self, file_path: str, content: str) -> None:
        """Create a new file with given content."""
        try:
            path = Path(file_path).resolve()
            self._validate_path(path)
            
            if path.exists():
                raise FileExistsError(f"File already exists: {path}")
            
            parent_dir = path.parent
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
        except (ValueError, FileExistsError, IOError) as e:
            raise ValueError(f"Error creating file: {str(e)}")

    def delete_file(self, file_path: str) -> None:
        """Delete a file."""
        try:
            path = Path(file_path).resolve()
            self._validate_path(path)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            if not path.is_file():
                raise ValueError(f"Not a file: {path}")
            
            path.unlink()
        except (ValueError, FileNotFoundError, IOError) as e:
            raise ValueError(f"Error deleting file: {str(e)}")

# Example usage:
if __name__ == "__main__":
    try:
        # Initialize FileManager with a specific base directory
        file_manager = FileManager("/path/to/base/directory")
        
        # Example operations
        try:
            # Create a file
            file_manager.create_file("example.txt", "Hello, World!")
            print("File created successfully")
            
            # View file
            content = file_manager.view_file("example.txt")
            print(f"File content: {content}")
            
            # Delete file
            file_manager.delete_file("example.txt")
            print("File deleted successfully")
        except ValueError as e:
            print(f"Operation failed: {str(e)}")
    except ValueError as e:
        print(f"Initialization failed: {str(e)}")