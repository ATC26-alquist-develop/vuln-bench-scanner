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
        
        # Verify base directory permissions
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Insufficient permissions for base directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory components and invalid characters
        sanitized = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)
        if not sanitized:
            sanitized = "note"
        return sanitized

    def _get_secure_path(self, filename: str) -> pathlib.Path:
        """Get secure file path with random name."""
        safe_name = self._sanitize_filename(filename)
        random_suffix = secrets.token_hex(8)
        return (self.base_dir / f"{safe_name}_{random_suffix}").with_suffix(".txt")

    def add_note(self, note_text: str) -> Optional[pathlib.Path]:
        """Add a new note securely."""
        if not note_text or not isinstance(note_text, str):
            raise ValueError("Invalid note content")

        # Sanitize note content
        note_text = re.sub(r'[^a-zA-Z0-9\s\.\?\!\-\'\"]', '', note_text)

        try:
            file_path = self._get_secure_path(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{note_text[:50]}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(note_text)
            return file_path
        except (IOError, OSError) as e:
            raise IOError(f"Failed to write note: {str(e)}")

    def read_note(self, file_path: pathlib.Path) -> Optional[str]:
        """Read a note securely."""
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError("Note file not found")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, OSError) as e:
            raise IOError(f"Failed to read note: {str(e)}")

    def list_notes(self) -> list[pathlib.Path]:
        """List all notes in the directory."""
        return [f for f in self.base_dir.iterdir() if f.is_file()]

# Example usage
if __name__ == "__main__":
    try:
        note_taker = SecureNoteTaker()
        # Add a note
        note_path = note_taker.add_note("Hello, this is a test note.")
        print(f"Note added to: {note_path}")

        # Read the note
        note_content = note_taker.read_note(note_path)
        print(f"Note content: {note_content}")

        # List all notes
        notes = note_taker.list_notes()
        print("All notes:")
        for note in notes:
            print(f"- {note.name}")
    except Exception as e:
        print(f"Error: {str(e)}")