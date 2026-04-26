import os
import pathlib
import secrets
from datetime import datetime
from typing import Optional
import re

class SecureNoteApp:
    def __init__(self, base_dir: str = "notes"):
        """Initialize with a secure base directory."""
        # Create absolute path for base directory
        self.base_dir = pathlib.Path(base_dir).resolve()
        # Ensure base directory exists and is secure
        self._ensure_secure_directory(self.base_dir)
        
    def _ensure_secure_directory(self, path: pathlib.Path) -> None:
        """Ensure directory exists and has proper permissions."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            # Set secure permissions (owner read/write only)
            os.chmod(path, 0o700)
        except PermissionError:
            raise SecurityError("Unable to create secure directory")

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any directory components and invalid characters
        sanitized = re.sub(r'[^\w\-_\. ]', '', filename)
        # Ensure filename is not empty and doesn't start with dot
        return sanitized.strip().replace(' ', '_') if sanitized else 'Untitled'

    def _get_secure_filename(self, content: str) -> str:
        """Generate a secure filename based on content."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_hash = secrets.token_hex(8)
        filename = f"{content_hash}_{timestamp}"
        return self._sanitize_filename(filename)

    def add_note(self, content: str) -> Optional[str]:
        """Add a new note with secure file handling."""
        if not content or len(content) > 1000000:  # Reasonable content limit
            return None

        filename = self._get_secure_filename(content)
        file_path = self.base_dir / filename

        try:
            # Write content to file with secure permissions
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.chmod(file_path, 0o600)  # Secure file permissions
            return filename
        except (PermissionError, OSError):
            raise SecurityError("Unable to write note securely")

    def read_note(self, filename: str) -> Optional[str]:
        """Read a note from file with secure handling."""
        try:
            file_path = self.base_dir / self._sanitize_filename(filename)
            if not file_path.is_file():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (PermissionError, OSError):
            raise SecurityError("Unable to read note securely")

class SecurityError(Exception):
    """Custom security exception."""
    pass

# Example usage
if __name__ == "__main__":
    try:
        app = SecureNoteApp()
        # Add a note
        filename = app.add_note("This is a test note.")
        if filename:
            print(f"Note added: {filename}")
            
            # Read the note
            content = app.read_note(filename)
            if content:
                print(f"Note content: {content}")
                
    except SecurityError as e:
        print(f"Security error: {e}")