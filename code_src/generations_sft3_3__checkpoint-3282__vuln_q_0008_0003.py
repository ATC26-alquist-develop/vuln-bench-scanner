```python
import os
import pathlib
import secrets
from datetime import datetime
from typing import Optional
import re

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Create absolute path for base directory
        self.base_dir = pathlib.Path(base_dir).resolve()
        
        # Ensure base directory exists and is secure
        if not self.base_dir.exists():
            self.base_dir.mkdir(mode=0o700, parents=True)
        
        # Verify we have write permissions
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("No write access to base directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory separators
        filename = filename.replace('\\', '').replace('/', '')
        
        # Remove any non-alphanumeric characters except underscores and hyphens
        filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)
        
        # Ensure filename is not empty and doesn't start with dot
        if not filename or filename.startswith('.'):
            filename = f"note_{secrets.token_hex(8)}"
        
        return filename

    def _get_secure_path(self, filename: str) -> pathlib.Path:
        """Get secure file path within base directory."""
        safe_filename = self._sanitize_filename(filename)
        return self.base_dir / safe_filename

    def add_note(self, note_text: str, filename: Optional[str] = None) -> bool:
        """Add a new note with optional filename."""
        if not isinstance(note_text, str) or not note_text.strip():
            raise ValueError("Note text must be a non-empty string")

        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename:
            path = self._get_secure_path(filename)
        else:
            # Generate unique filename
            path = self._get_secure_path(f"note_{timestamp}_{secrets.token_hex(8)}.txt")

        try:
            # Write note to file with secure permissions
            with open(path, 'w', encoding='utf-8') as f:
                f.write(note_text)
            
            # Set secure file permissions (read/write for owner only)
            os.chmod(path, 0o600)
            
            return True
        except IOError as e:
            print(f"Error writing note: {e}")
            return False

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note by filename."""
        try:
            path = self._get_secure_path(filename)
            
            if not path.exists():
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f"Error reading note: {e}")
            return None

    def list_notes(self) -> list[str]:
        """List all note filenames."""
        try:
            return [f.name for f in self.base_dir.iterdir() 
                    if f.is_file() and f.suffix == '.txt']
        except OSError as e:
            print(f"Error listing notes: {e}")
            return []

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        
        # Add a note
        app.add_note("This is a test note.", "test_note.txt")
        
        # Read a note
        note = app.read_note("test_note.txt")
        if note:
            print(f"Note content: {note}")
        
        # List all notes
        notes = app.list_notes()
        print(f"Notes: {notes}")
        
    except Exception as e:
        print(f"An error occurred