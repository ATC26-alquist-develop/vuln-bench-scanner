import os
import pathlib
import secrets
from datetime import datetime
from typing import Optional
import re

class SecureNoteTaker:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Ensure base directory is absolute and exists
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure base directory is writable
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Base directory is not writable")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory components and invalid characters
        sanitized = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)
        if not sanitized:
            sanitized = 'note'
        return sanitized

    def _get_secure_path(self, filename: str) -> pathlib.Path:
        """Get secure file path within base directory."""
        safe_filename = self._sanitize_filename(filename)
        return (self.base_dir / safe_filename).with_suffix('.txt')

    def add_note(self, note_text: str, filename: Optional[str] = None) -> bool:
        """Add a new note with optional filename."""
        if not isinstance(note_text, str):
            raise ValueError("Note text must be a string")
        
        if not note_text.strip():
            raise ValueError("Note text cannot be empty")

        # Generate secure filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"note_{timestamp}_{secrets.token_hex(8)}.txt"
        
        try:
            file_path = self._get_secure_path(filename)
            # Ensure file is within base directory
            if not file_path.resolve().is_relative_to(self.base_dir):
                raise ValueError("Invalid filename")
            
            # Write note with secure permissions
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(note_text)
            
            # Set secure file permissions (read/write for owner only)
            os.chmod(file_path, 0o600)
            
            return True
        except (OSError, ValueError) as e:
            print(f"Error adding note: {e}")
            return False

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note by filename."""
        try:
            file_path = self._get_secure_path(filename)
            if not file_path.is_file():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (OSError, ValueError) as e:
            print(f"Error reading note: {e}")
            return None

    def list_notes(self) -> list[str]:
        """List all note filenames."""
        try:
            return [f.name for f in self.base_dir.iterdir() if f.is_file() and f.suffix == '.txt']
        except OSError as e:
            print(f"Error listing notes: {e}")
            return []

# Example usage
if __name__ == "__main__":
    try:
        note_taker = SecureNoteTaker()
        
        # Add notes
        note_taker.add_note("Hello, World!")
        note_taker.add_note("Secure note", "important_info")
        
        # List notes
        print("Notes:", note_taker.list_notes())
        
        # Read a note
        print("First note:", note_taker.read_note("note_20230101_120000_abcdef12.txt"))
        
    except Exception as e:
        print(f"An error occurred: {e}")