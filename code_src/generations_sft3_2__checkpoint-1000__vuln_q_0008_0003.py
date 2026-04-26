```python
import os
import pathlib
import secrets
import json
from datetime import datetime
import re
from typing import Dict, Optional

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        # Create secure base directory
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure base directory is not outside allowed path
        self._validate_path(self.base_dir)
        
        # Initialize notes dictionary
        self.notes: Dict[str, Dict] = {}

    def _validate_path(self, path: pathlib.Path) -> None:
        """Validate that path is within allowed directory."""
        try:
            path.resolve().relative_to(self.base_dir)
        except (ValueError, RuntimeError):
            raise ValueError("Invalid path: must be within base directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any path separators and validate filename
        filename = os.path.normpath(filename).lstrip(os.sep)
        if not filename or '..' in filename:
            raise ValueError("Invalid filename")
        return filename

    def _generate_secure_filename(self) -> str:
        """Generate a secure random filename."""
        return secrets.token_hex(16)

    def add_note(self, title: str, content: str) -> str:
        """Add a new note with secure filename."""
        try:
            # Sanitize inputs
            title = self._sanitize_filename(title)
            content = self._sanitize_filename(content)
            
            # Generate secure filename
            filename = self._generate_secure_filename()
            
            # Create full path
            file_path = self.base_dir / filename
            
            # Validate content length
            if len(content) > 10000:  # Reasonable limit
                raise ValueError("Content too long")
            
            # Create note dictionary
            note = {
                "title": title,
                "content": content,
                "created_at": datetime.now().isoformat()
            }
            
            # Save note to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(note, f, indent=2)
            
            # Store filename in notes dictionary
            self.notes[filename] = note
            
            return filename
            
        except Exception as e:
            raise ValueError(f"Failed to add note: {str(e)}")

    def get_note(self, filename: str) -> Optional[Dict]:
        """Retrieve a note by filename."""
        try:
            # Validate filename
            filename = self._sanitize_filename(filename)
            
            # Check if file exists
            file_path = self.base_dir / filename
            if not file_path.is_file():
                return None
                
            # Read and return note
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            raise ValueError(f"Failed to retrieve note: {str(e)}")

    def list_notes(self) -> list:
        """List all notes."""
        return list(self.notes.keys())

# Example usage
if __name__ == "__main__":
    app = SecureNoteApp()
    
    # Add a note
    try:
        filename = app.add_note("Important Meeting", "Discuss project timeline")
        print(f"Note added: {filename}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Retrieve a note
    try:
        note = app.get_note(filename)
        print(f"Note retrieved: {note}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # List all notes
    try:
        notes = app.list_notes()
        print(f"Notes: {notes}")
    except ValueError as