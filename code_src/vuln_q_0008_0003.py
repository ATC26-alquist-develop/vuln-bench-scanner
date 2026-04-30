import os
import re
from pathlib import Path
import hashlib
import json
from typing import Dict, Optional

class SecureNoteApp:
    def __init__(self, storage_path: str = "./notes"):
        """Initialize the note app with a secure storage path."""
        # Validate and create storage path securely
        self.storage_path = Path(storage_path).resolve()
        if not self.storage_path.exists():
            self.storage_path.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _validate_note_content(self, content: str) -> bool:
        """Validate note content for security."""
        # Prevent path traversal and ensure content is safe
        if not content or not isinstance(content, str):
            return False
        # Remove any potentially dangerous characters
        content = re.sub(r'[^\w\s.,!?-]', '', content)
        return True

    def _sanitize_filename(self, filename: str) -> str:
        """Create a secure filename from the note title."""
        # Remove any potentially dangerous characters and normalize
        filename = re.sub(r'[^\w\-\.]', '_', filename)
        # Ensure filename is unique and doesn't expose system information
        filename = hashlib.sha256(filename.encode()).hexdigest()[:12] + '.txt'
        return filename

    def create_note(self, title: str, content: str) -> None:
        """Create a new note securely."""
        if not self._validate_note_content(content):
            raise ValueError("Invalid note content")

        filename = self._sanitize_filename(title)
        file_path = self.storage_path / filename

        try:
            # Use atomic write to prevent partial files
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump({"title": title, "content": content}, f)
            temp_path.replace(file_path)
        except Exception as e:
            raise RuntimeError(f"Failed to create note: {str(e)}")

    def read_note(self, title: str) -> Optional[str]:
        """Read a note securely."""
        filename = self._sanitize_filename(title)
        file_path = self.storage_path / filename

        try:
            if not file_path.exists():
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                note = json.load(f)
            return f"Title: {note['title']}\nContent: {note['content']}"
        except Exception as e:
            raise RuntimeError(f"Failed to read note: {str(e)}")

    def list_notes(self) -> None:
        """List all notes securely."""
        try:
            for note_file in self.storage_path.glob('*.txt'):
                title = note_file.stem
                print(f"{title}")
        except Exception as e:
            raise RuntimeError(f"Failed to list notes: {str(e)}")

# Example usage
if __name__ == "__main__":
    app = SecureNoteApp()
    try:
        app.create_note("Meeting Notes", "Discuss project timeline")
        app.create_note("Shopping List", "Apples, Bananas, Milk")
        print(app.read_note("Meeting Notes"))
        print(app.read_note("Shopping List"))
        print(app.read_note("Nonexistent Note"))
        print(app.list_notes())
    except Exception as e:
        print(f"Error: {str(e)}")