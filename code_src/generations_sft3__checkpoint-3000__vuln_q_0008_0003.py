import os
import pathlib
from datetime import datetime
import secrets
import re
from typing import Optional

class SecureNoteApp:
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
        # Remove any directory separators
        filename = os.path.normpath(filename).lstrip(os.sep)
        # Replace invalid characters with underscore
        filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
        # Ensure filename is not empty
        if not filename:
            filename = "note"
        return filename

    def _get_secure_filename(self, content: str) -> str:
        """Generate a secure filename based on content."""
        # Create a random component
        random_suffix = secrets.token_hex(8)
        # Combine content with random suffix
        return f"{self._sanitize_filename(content[:50])}_{random_suffix}.txt"

    def add_note(self, content: str) -> Optional[str]:
        """Add a new note securely."""
        if not content or len(content) > 10000:  # Reasonable content limits
            return None

        filename = self._get_secure_filename(content)
        filepath = self.base_dir / filename

        try:
            # Ensure we're not overwriting existing files
            if filepath.exists():
                return None

            # Write file with secure permissions
            with open(filepath, 'w', encoding='utf-8') as f:
                os.chmod(filepath, 0o600)  # Read/write for owner only
                f.write(content)
            return filename
        except (IOError, OSError):
            return None

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note securely."""
        filepath = self.base_dir / self._sanitize_filename(filename)

        try:
            if not filepath.exists():
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, OSError):
            return None

    def delete_note(self, filename: str) -> bool:
        """Delete a note securely."""
        filepath = self.base_dir / self._sanitize_filename(filename)

        try:
            if not filepath.exists():
                return False

            filepath.unlink()
            return True
        except (IOError, OSError):
            return False

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        
        # Add a note
        note = "This is a test note."
        filename = app.add_note(note)
        if filename:
            print(f"Note added: {filename}")
        
        # Read the note
        content = app.read_note(filename)
        if content:
            print(f"Note content: {content}")
        
        # Delete the note
        if app.delete_note(filename):
            print("Note deleted successfully")
        else:
            print("Failed to delete note")
            
    except Exception as e:
        print(f"An error occurred: {e}")