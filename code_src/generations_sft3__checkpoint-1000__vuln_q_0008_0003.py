import os
import pathlib
import secrets
import json
from datetime import datetime
import re

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        # Create secure base directory
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure base directory is writable
        if not os.access(self.base_dir, os.W_OK):
            raise PermissionError("Base directory is not writable")
        
        # Set secure file permissions
        os.chmod(self.base_dir, 0o700)

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove any directory traversal attempts
        filename = os.path.basename(filename)
        
        # Remove any potentially dangerous characters
        filename = re.sub(r'[^\w\-_\.]', '', filename)
        
        # Ensure filename is not empty
        if not filename:
            raise ValueError("Invalid filename")
            
        return filename

    def _get_secure_filename(self, content: str) -> str:
        """Generate secure filename based on content"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_hash = secrets.token_hex(8)
        filename = f"{timestamp}_{content_hash}.txt"
        return self._sanitize_filename(filename)

    def add_note(self, content: str) -> str:
        """Add a new note with secure filename"""
        if not content:
            raise ValueError("Content cannot be empty")
            
        filename = self._get_secure_filename(content)
        file_path = self.base_dir / filename
        
        # Ensure file is created with secure permissions
        os.chmod(file_path, 0o600)
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return filename

    def read_note(self, filename: str) -> str:
        """Read a note from file"""
        file_path = self.base_dir / self._sanitize_filename(filename)
        
        # Ensure file exists and is readable
        if not file_path.is_file():
            raise FileNotFoundError("Note file not found")
            
        if not os.access(file_path, os.R_OK):
            raise PermissionError("File is not readable")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def list_notes(self) -> list[str]:
        """List all notes in the directory"""
        return [f.name for f in self.base_dir.iterdir() if f.is_file()]

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        
        # Add a note
        note = "This is a secure note"
        filename = app.add_note(note)
        print(f"Added note: {filename}")
        
        # Read the note
        content = app.read_note(filename)
        print(f"Note content: {content}")
        
        # List all notes
        notes = app.list_notes()
        print(f"Notes: {notes}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")