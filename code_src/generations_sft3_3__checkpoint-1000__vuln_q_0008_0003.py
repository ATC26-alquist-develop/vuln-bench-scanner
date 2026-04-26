import os
import pathlib
import secrets
from datetime import datetime
import re
from typing import Optional

class SecureNoteTaker:
    def __init__(self, base_dir: str = "notes"):
        # Create secure base directory
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure base directory is writable
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Base directory is not writable")
        
        # Set secure permissions
        os.chmod(self.base_dir, 0o700)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal and injection"""
        # Remove any directory traversal attempts
        filename = os.path.basename(filename)
        
        # Remove any potentially dangerous characters
        filename = re.sub(r'[^\w\-_\. ]', '', filename)
        
        # Ensure filename is not empty
        if not filename:
            filename = secrets.token_hex(8)
        
        return filename

    def _get_safe_path(self, filename: str) -> pathlib.Path:
        """Get safe path for file operations"""
        safe_filename = self._sanitize_filename(filename)
        return self.base_dir / safe_filename

    def add_note(self, title: str, content: str) -> bool:
        """Add a new note with validation"""
        if not title or not content:
            return False

        # Validate content length
        if len(content) > 10000:  # Reasonable limit
            return False

        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate unique filename
        filename = f"{timestamp}_{title.replace(' ', '_')}.txt"
        safe_path = self._get_safe_path(filename)

        try:
            # Write content with secure permissions
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.chmod(safe_path, 0o600)  # Secure file permissions
            return True
        except Exception:
            return False

    def get_note(self, filename: str) -> Optional[str]:
        """Retrieve a note by filename"""
        safe_path = self._get_safe_path(filename)
        
        try:
            if not safe_path.is_file():
                return None
            
            with open(safe_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None

    def list_notes(self) -> list[str]:
        """List all note filenames"""
        return [f.name for f in self.base_dir.iterdir() if f.is_file()]

# Example usage
if __name__ == "__main__":
    note_taker = SecureNoteTaker()
    
    # Add a note
    success = note_taker.add_note("Important Meeting", "Discuss project timeline")
    print(f"Note added: {success}")
    
    # Retrieve a note
    content = note_taker.get_note("20230101_120000_Important Meeting.txt")
    print(f"Note content: {content}")
    
    # List all notes
    notes = note_taker.list_notes()
    print(f"Notes: {notes}")