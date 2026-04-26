import os
import pathlib
import secrets
from datetime import datetime
from typing import Optional
import re

class SecureNoteTaker:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Ensure base directory exists and is secure
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure base directory is writable
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Base directory is not writable")
        
        # Ensure base directory is not in sensitive locations
        if any(p in str(self.base_dir) for p in ['/etc', '/var', '/usr', '/bin']):
            raise SecurityError("Base directory cannot be in system directories")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory components and invalid characters
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        if not sanitized:
            sanitized = 'note'
        return sanitized

    def _get_secure_path(self, filename: str) -> pathlib.Path:
        """Get secure file path with random name."""
        safe_name = self._sanitize_filename(filename)
        random_suffix = secrets.token_hex(8)
        return (self.base_dir / f"{safe_name}_{random_suffix}").resolve()

    def add_note(self, note: str, filename: Optional[str] = None) -> pathlib.Path:
        """Add a new note with optional filename."""
        if not isinstance(note, str):
            raise ValueError("Note must be a string")
        
        if not note.strip():
            raise ValueError("Note cannot be empty")

        # Sanitize filename if provided
        if filename:
            path = self._get_secure_path(filename)
        else:
            # Generate random filename
            path = self._get_secure_path(f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

        # Ensure file is within base directory
        if self.base_dir not in path.parents:
            raise SecurityError("Invalid file path")

        # Write note to file with secure permissions
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(note)
            os.chmod(path, 0o600)  # Read/write for owner only
        except IOError as e:
            raise IOError(f"Failed to write note: {e}")

        return path

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note by filename."""
        path = self._get_secure_path(filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return None

    def delete_note(self, filename: str) -> bool:
        """Delete a note by filename."""
        path = self._get_secure_path(filename)
        try:
            os.remove(path)
            return True
        except OSError:
            return False

class SecurityError(Exception):
    """Custom security exception."""
    pass

# Example usage
if __name__ == "__main__":
    try:
        note_taker = SecureNoteTaker()
        note_taker.add_note("Hello, World!", "test_note")
        content = note_taker.read_note("test_note")
        print(f"Note content: {content}")
        note_taker.delete_note("test_note")
    except Exception as e:
        print(f"Error: {e}")