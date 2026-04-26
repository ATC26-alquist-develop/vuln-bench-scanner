import os
from pathlib import Path
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with file path and validate it's safe."""
        self.file_path = Path(file_path).resolve()
        self._validate_path()

    def _validate_path(self) -> None:
        """Validate file path is safe and within allowed directory."""
        try:
            # Check if path is absolute
            if not self.file_path.is_absolute():
                raise ValueError("File path must be absolute")
            
            # Check if path is within allowed directory
            allowed_dir = Path.home() / "secure_files"
            if not str(self.file_path).startswith(str(allowed_dir)):
                raise ValueError("File path must be within allowed directory")
            
            # Check if file exists
            if not self.file_path.exists():
                raise FileNotFoundError(f"File {self.file_path} does not exist")
            
            # Check if file is a regular file
            if not self.file_path.is_file():
                raise ValueError(f"{self.file_path} is not a regular file")
            
        except Exception as e:
            raise ValueError(f"Invalid file path: {str(e)}")

    def read_file(self) -> Optional[str]:
        """Securely read file contents."""
        try:
            if not self.file_path.exists():
                return None
                
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return None

    def write_file(self, content: str) -> bool:
        """Securely write content to file."""
        try:
            # Create parent directory if it doesn't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content with proper encoding
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception:
            return False

    def delete_file(self) -> bool:
        """Securely delete file."""
        try:
            if not self.file_path.exists():
                return False
                
            self.file_path.unlink()
            return True
        except Exception:
            return False