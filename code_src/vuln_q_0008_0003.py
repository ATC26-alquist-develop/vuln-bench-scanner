```python
import os
import pathlib
import tempfile
import shutil
from cryptography.fernet import Fernet
import getpass

class SecureNoteApp:
    def __init__(self, base_dir):
        """Initialize secure note app with encrypted storage."""
        self.base_dir = pathlib.Path(base_dir).resolve()
        self.key = self._generate_key()
        self.fernet = Fernet(self.key)
        self._secure_temp_dir()

    def _secure_temp_dir(self):
        """Create secure temporary directory for notes."""
        try:
            self.temp_dir = tempfile.mkdtemp(dir=self.base_dir)
        except OSError:
            raise SecurityError("Failed to create secure temporary directory")

    def _generate_key(self):
        """Generate secure encryption key."""
        return Fernet.generate_key()

    def _secure_filename(self, filename):
        """Create secure filename from user input."""
        return pathlib.Path(filename).name

    def add_note(self, title, content):
        """Add a new note securely."""
        safe_title = self._secure_filename(title)
        safe_content = self.fernet.encrypt(content.encode()).decode()
        note_path = self.temp_dir / f"{safe_title}.txt"
        try:
            with open(note_path, 'w') as f:
                f.write(safe_content)
        except IOError:
            raise SecurityError("Failed to write note securely")

    def get_note(self, title):
        """Retrieve a note securely."""
        safe_title = self._secure_filename(title)
        note_path = self.temp_dir / f"{safe_title}.txt"
        if not note_path.exists():
            raise SecurityError("Note not found")
        try:
            with open(note_path, 'r') as f:
                encrypted_content = f.read()
            return self.fernet.decrypt(encrypted_content.encode()).decode()
        except (IOError, ValueError):
            raise SecurityError("Failed to read note securely")

    def delete_note(self, title):
        """Delete a note securely."""
        safe_title = self._secure_filename(title)
        note_path = self.temp_dir / f"{safe_title}.txt"
        if not note_path.exists():
            raise SecurityError("Note not found")
        try:
            os.remove(note_path)
        except OSError:
            raise SecurityError("Failed to delete note securely")

    def __del__(self):
        """Securely clean up temporary directory."""
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except OSError:
            pass  # Ignore errors during cleanup

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass
```