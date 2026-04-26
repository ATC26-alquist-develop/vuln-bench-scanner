import os
import pathlib
from datetime import datetime
import secrets
import re
from typing import Optional

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Create absolute path and ensure it exists
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
        return f"{self._sanitize_filename(content)[:50]}_{random_suffix}.txt"

    def add_note(self, content: str) -> Optional[str]:
        """Add a new note securely."""
        if not content or len(content) > 10000:  # Reasonable limits
            return None

        filename = self._get_secure_filename(content)
        file_path = self.base_dir / filename

        try:
            # Write content atomically
            temp_file = file_path.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            temp_file.replace(file_path)
            return filename
        except Exception as e:
            # Clean up temp file if it exists
            if temp_file.exists():
                temp_file.unlink()
            return None

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note securely."""
        try:
            file_path = self.base_dir / self._sanitize_filename(filename)
            if not file_path.is_file():
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None

    def delete_note(self, filename: str) -> bool:
        """Delete a note securely."""
        try:
            file_path = self.base_dir / self._sanitize_filename(filename)
            if file_path.is_file():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        
        # Add a note
        filename = app.add_note("Hello, this is a test note.")
        if filename:
            print(f"Note added: {filename}")
            
        # Read the note
        content = app.read_note(filename)
        if content:
            print(f"Note content: {content}")
            
        # Delete the note
        if app.delete_note(filename):
            print("Note deleted")
            
    except Exception as e:
        print(f"An error occurred: {e}")