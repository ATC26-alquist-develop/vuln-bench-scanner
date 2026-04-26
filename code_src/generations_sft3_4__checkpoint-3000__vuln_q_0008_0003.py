import os
import pathlib
from datetime import datetime
import secrets
import re
from typing import Optional

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Create absolute path for base directory
        self.base_dir = pathlib.Path(base_dir).resolve()
        # Ensure base directory exists and is secure
        self._ensure_secure_directory(self.base_dir)
        
    def _ensure_secure_directory(self, path: pathlib.Path) -> None:
        """Ensure directory exists and has proper permissions."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            # Set secure permissions (owner read/write only)
            os.chmod(path, 0o700)
        except PermissionError:
            raise SecurityError("Unable to create secure directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory components and invalid characters
        sanitized = re.sub(r'[^\w\-_\. ]', '', filename)
        # Ensure filename is not empty and has a valid extension
        if not sanitized or not sanitized.endswith('.txt'):
            sanitized = f"note_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(8)}.txt"
        return sanitized

    def add_note(self, content: str) -> str:
        """Add a new note with a secure filename."""
        if not content or not isinstance(content, str):
            raise ValueError("Invalid content")
            
        filename = self._sanitize_filename(f"note_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(8)}.txt")
        filepath = self.base_dir / filename

        try:
            # Write with secure permissions (owner read/write only)
            with open(filepath, 'w', encoding='utf-8') as f:
                os.chmod(filepath, 0o600)
                f.write(content)
            return str(filepath)
        except PermissionError:
            raise SecurityError("Unable to write secure file")

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note from a secure file."""
        try:
            filepath = self.base_dir / self._sanitize_filename(filename)
            if not filepath.is_file():
                return None
                
            # Check file permissions
            if not os.access(filepath, os.R_OK):
                raise SecurityError("File not readable")
                
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except (PermissionError, FileNotFoundError):
            return None

class SecurityError(Exception):
    """Custom security exception."""
    pass

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        # Add a note
        note_path = app.add_note("This is a test note.")
        print(f"Note added: {note_path}")
        
        # Read the note
        content = app.read_note(os.path.basename(note_path))
        if content:
            print(f"Note content: {content}")
        else:
            print("Note not found or unreadable")
            
    except SecurityError as e:
        print(f"Security error: {e}")