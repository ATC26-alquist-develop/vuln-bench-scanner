import os
import pathlib
from datetime import datetime
import secrets
import re
from typing import Optional

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        """Initialize the note-taking app with a secure base directory."""
        # Ensure base directory is absolute and exists
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Verify base directory permissions
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Insufficient permissions for note directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal attacks."""
        # Remove any directory separators and limit length
        safe_name = re.sub(r'[\\/:"*?<>|]', '', filename)
        safe_name = safe_name[:255]  # Limit filename length
        
        # Ensure filename is not empty
        if not safe_name:
            safe_name = "note"
        
        return safe_name

    def _get_secure_path(self, filename: str) -> pathlib.Path:
        """Get a secure path for a note file."""
        safe_name = self._sanitize_filename(filename)
        return (self.base_dir / safe_name).with_suffix('.txt')

    def add_note(self, note_text: str) -> Optional[str]:
        """Add a new note securely."""
        if not note_text or not isinstance(note_text, str):
            return None

        # Sanitize and limit note content
        note_text = re.sub(r'[^\w\s\.\,\?\!\-\'\"]', '', note_text)
        note_text = note_text[:10000]  # Limit note length

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(8)
        
        filename = f"note_{timestamp}_{random_suffix}.txt"
        path = self._get_secure_path(filename)
        
        try:
            # Write note to file with secure permissions
            with open(path, 'w', encoding='utf-8') as f:
                f.write(note_text)
            os.chmod(path, 0o600)  # Set secure file permissions
            
            return filename
        except IOError as e:
            print(f"Error writing note: {e}")
            return None

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note securely."""
        try:
            path = self._get_secure_path(filename)
            if not path.exists():
                return None
                
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f"Error reading note: {e}")
            return None

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        new_note = app.add_note("This is a test note.")
        if new_note:
            print(f"Added note: {new_note}")
            read_note = app.read_note(new_note)
            if read_note:
                print(f"Note content: {read_note}")
    except Exception as e:
        print(f"An error occurred: {e}")