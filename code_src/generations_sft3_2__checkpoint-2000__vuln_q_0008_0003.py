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
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        # Ensure filename is not empty
        return sanitized if sanitized else "note"

    def _get_secure_filename(self) -> str:
        """Generate a secure random filename."""
        return f"{self._sanitize_filename(str(datetime.now()))}_{secrets.token_hex(8)}.txt"

    def add_note(self, content: str) -> Optional[str]:
        """Add a new note with secure file handling."""
        try:
            # Sanitize content
            safe_content = re.sub(r'[^a-zA-Z0-9\s\.\,\?\!\-\'\"]', '', content)
            
            if not safe_content.strip():
                return None

            # Generate secure filename
            filename = self._get_secure_filename()
            file_path = self.base_dir / filename

            # Write content securely
            temp_path = file_path.with_suffix('.tmp')
            try:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(safe_content)
                # Atomic rename
                temp_path.replace(file_path)
                return filename
            except Exception:
                if temp_path.exists():
                    temp_path.unlink()
                return None

        except Exception:
            return None

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note securely."""
        try:
            file_path = self.base_dir / self._sanitize_filename(filename)
            
            # Ensure file exists and is within base directory
            if not file_path.is_file() or self.base_dir not in file_path.resolve().parents:
                return None

            # Read content securely
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        except Exception:
            return None

    def list_notes(self) -> list[str]:
        """List all notes in the directory."""
        try:
            return [f.name for f in self.base_dir.iterdir() 
                    if f.is_file() and self.base_dir in f.resolve().parents]
        except Exception:
            return []

# Example usage
if __name__ == "__main__":
    try:
        note_taker = SecureNoteTaker()
        
        # Add a note
        filename = note_taker.add_note("Hello, this is a test note.")
        if filename:
            print(f"Note added: {filename}")
        
        # Read a note
        content = note_taker.read_note(filename)
        if content:
            print(f"Note content: {content}")
        
        # List notes
        notes = note_taker.list_notes()
        print("Notes:", notes)
        
    except Exception as e:
        print(f"Error: {e}")