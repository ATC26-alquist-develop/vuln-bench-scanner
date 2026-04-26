import os
from pathlib import Path
import logging
from typing import Optional

class SecureFileHandler:
    def __init__(self, file_path: str):
        """Initialize with file path and set up logging."""
        self.file_path = Path(file_path).resolve()
        self.logger = logging.getLogger(__name__)
        
        # Ensure the file path is within allowed directory
        allowed_dir = Path.cwd()
        if not self.file_path.is_relative_to(allowed_dir):
            raise ValueError("File path must be within current working directory")
            
        # Ensure file has .txt extension
        if not self.file_path.suffix.lower() == '.txt':
            raise ValueError("File must have .txt extension")

    def read_file(self) -> Optional[str]:
        """Securely read file contents."""
        try:
            if not self.file_path.exists():
                self.logger.warning(f"File not found: {self.file_path}")
                return None

            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.logger.info(f"Successfully read file: {self.file_path}")
            return content
        except Exception as e:
            self.logger.error(f"Error reading file: {str(e)}")
            return None

    def write_file(self, content: str) -> bool:
        """Securely write content to file."""
        try:
            # Ensure content is a string
            if not isinstance(content, str):
                raise ValueError("Content must be a string")

            # Create parent directory if it doesn't exist
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content with proper encoding
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            self.logger.info(f"Successfully wrote to file: {self.file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing to file: {str(e)}")
            return False

    def delete_file(self) -> bool:
        """Securely delete the file."""
        try:
            if not self.file_path.exists():
                self.logger.warning(f"File not found for deletion: {self.file_path}")
                return False

            self.file_path.unlink()
            self.logger.info(f"Successfully deleted file: {self.file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting file: {str(e)}")
            return False