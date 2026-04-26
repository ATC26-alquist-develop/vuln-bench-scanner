import os
import pathlib
from datetime import datetime
import secrets
import re
from typing import Optional

class SecureNoteTaker:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Ensure base directory is absolute and exists
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure base directory is writable
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Cannot write to base directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory separators
        filename = os.path.normpath(filename).lstrip(os.sep)
        # Replace invalid characters with underscore
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        # Ensure filename is not empty
        if not filename:
            filename = "note"
        return filename

    def _get_secure_filename(self, content: str) -> str:
        """Generate a secure filename based on content."""
        # Create a random component
        random_component = secrets.token_hex(8)
        # Combine content with random component
        content_hash = hash(content)
        filename = f"{content_hash}_{random_component}.txt"
        return self._sanitize_filename(filename)

    def add_note(self, content: str) -> Optional[str]:
        """Add a new note securely."""
        if not content or len(content) > 1000000:  # Reasonable limit
            return None

        filename = self._get_secure_filename(content)
        file_path = self.base_dir / filename

        try:
            # Write file with secure permissions
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.chmod(file_path, 0o600)  # Read/write for owner only
            
            # Create timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"Note added: {filename} at {timestamp}"
        except Exception as e:
            return f"Error adding note: {str(e)}"

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note securely."""
        if not filename or len(filename) > 255:
            return None

        file_path = self.base_dir / self._sanitize_filename(filename)

        try:
            if not file_path.is_file():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading note: {str(e)}"

    def list_notes(self) -> list[str]:
        """List all notes in the directory."""
        try:
            return [f.name for f in self.base_dir.iterdir() if f.is_file()]
        except Exception as e:
            return []

# Example usage
if __name__ == "__main__":
    try:
        note_taker = SecureNoteTaker()
        
        # Add a note
        result = note_taker.add_note("This is a test note.")
        print(result)

        # Read a note
        content = note_taker.read_note("test_note.txt")
        print(content)

        # List notes
        notes = note_taker.list_notes()
        print(notes)
    except Exception as e:
        print(f"Error: {str(e)}")