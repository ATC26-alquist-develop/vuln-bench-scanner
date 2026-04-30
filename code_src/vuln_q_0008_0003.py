import os
import pathlib
import tempfile
import shutil
from typing import Optional

class SecureNoteApp:
    def __init__(self, notes_dir: str):
        """Initialize with a secure notes directory."""
        # Validate and create notes directory
        self.notes_dir = pathlib.Path(notes_dir).resolve()
        if not self.notes_dir.exists():
            self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure the directory is writable only by the owner
        os.chmod(self.notes_dir, 0o700)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal attacks."""
        # Remove any path components and limit filename length
        return pathlib.Path(filename).name[:255].strip()

    def create_note(self, content: str) -> Optional[str]:
        """Create a new note securely."""
        if not content:
            return None

        # Sanitize filename
        safe_filename = self._sanitize_filename("note")
        
        # Create temporary file for atomic write
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=self.notes_dir) as temp_file:
            temp_path = temp_file.name
            
            try:
                # Write content to temporary file
                temp_file.write(content)
                temp_file.flush()
                
                # Atomic rename to final location
                os.replace(temp_path, self.notes_dir / f"{safe_filename}.txt")
                return f"Note created: {safe_filename}"
            except Exception:
                # Clean up temp file on error
                os.unlink(temp_path)
                return None

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note securely."""
        if not filename:
            return None

        # Sanitize filename
        safe_filename = self._sanitize_filename(filename)
        
        try:
            note_path = self.notes_dir / f"{safe_filename}.txt"
            if not note_path.is_file():
                return None
            with open(note_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception:
            return None

    def delete_note(self, filename: str) -> Optional[str]:
        """Delete a note securely."""
        if not filename:
            return None

        # Sanitize filename
        safe_filename = self._sanitize_filename(filename)
        
        try:
            note_path = self.notes_dir / f"{safe_filename}.txt"
            if not note_path.is_file():
                return None
            os.remove(note_path)
            return f"Note deleted: {safe_filename}"
        except Exception:
            return None

# Usage example
if __name__ == "__main__":
    app = SecureNoteApp("./secure_notes")
    
    # Create a note
    result = app.create_note("This is a secure note.")
    print(result)
    
    # Read a note
    content = app.read_note("note")
    print(content)
    
    # Delete a note
    result = app.delete_note("note")
    print(result)