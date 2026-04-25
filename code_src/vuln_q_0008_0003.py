import os
import pathlib
import tempfile
import shutil
from typing import Optional

class SecureNoteApp:
    def __init__(self, notes_dir: str):
        """Initialize with a secure notes directory."""
        # Create secure notes directory if it doesn't exist
        self.notes_dir = pathlib.Path(notes_dir).resolve()
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure the directory is writable and exists
        if not self.notes_dir.is_dir() or not os.access(self.notes_dir, os.W_OK):
            raise SecurityError("Invalid or inaccessible notes directory")

    def create_note(self, title: str, content: str) -> None:
        """Create a new note with title and content."""
        # Sanitize inputs
        title = self._sanitize_input(title)
        content = self._sanitize_input(content)
        
        # Create unique filename
        filename = f"{title.replace(' ', '_').lower()[:50]}.txt"
        filepath = self.notes_dir / filename
        
        # Create file securely
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=self.notes_dir) as temp_file:
                temp_file.write(content)
            shutil.move(temp_file.name, filepath)
        except (OSError, IOError) as e:
            raise SecurityError(f"Failed to create note: {str(e)}")

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note by filename."""
        filepath = self.notes_dir / filename
        
        # Validate file path
        if not filepath.is_file() or not filepath.suffix == '.txt':
            raise SecurityError("Invalid or non-existent note file")
            
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            raise SecurityError(f"Failed to read note: {str(e)}")

    def delete_note(self, filename: str) -> None:
        """Delete a note by filename."""
        filepath = self.notes_dir / filename
        
        # Validate file path
        if not filepath.is_file() or not filepath.suffix == '.txt':
            raise SecurityError("Invalid or non-existent note file")
            
        try:
            os.remove(filepath)
        except OSError as e:
            raise SecurityError(f"Failed to delete note: {str(e)}")

    @staticmethod
    def _sanitize_input(input_str: str) -> str:
        """Sanitize input to prevent path traversal attacks."""
        return ''.join(c for c in input_str if c.isalnum() or c in [' ', '_', '.', '-'])

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass