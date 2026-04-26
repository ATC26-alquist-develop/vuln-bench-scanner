import os
from pathlib import Path
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """
        Initialize secure file handler with path validation.
        
        Args:
            file_path: Path to the file
        """
        self.file_path = Path(file_path).resolve()
        self._validate_path()

    def _validate_path(self) -> None:
        """Validate file path to prevent directory traversal attacks."""
        if not self.file_path.exists():
            raise ValueError("File does not exist")
        if not self.file_path.is_file():
            raise ValueError("Path is not a file")
        if not os.access(self.file_path, os.R_OK | os.W_OK):
            raise PermissionError("Insufficient permissions")

    def read_file(self) -> Optional[str]:
        """
        Securely read file contents.
        
        Returns:
            File contents as string or None if error occurs
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file: {e}")
            return None

    def write_file(self, content: str) -> bool:
        """
        Securely write content to file.
        
        Args:
            content: Content to write to file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except IOError as e:
            print(f"Error writing to file: {e}")
            return False

# Example usage
if __name__ == "__main__":
    try:
        handler = SecureFileHandler("example.txt")
        content = handler.read_file()
        if content is not None:
            print("File contents:", content)
        
        handler.write_file("Hello, World!")
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")