import os
import secrets
import stat
from pathlib import Path
from typing import Optional

class SecureFileManager:
    def __init__(self, base_directory: str):
        """Initialize the file manager with a secure base directory."""
        self.base_directory = Path(base_directory).resolve()
        if not self.base_directory.is_dir():
            raise ValueError("Invalid base directory")
        self._set_secure_permissions()

    def _set_secure_permissions(self):
        """Set secure permissions on the base directory."""
        os.chmod(self.base_directory, stat.S_IRUSR | stat.S_IWUSR)

    def _is_safe_path(self, path: Path) -> bool:
        """Check if the path is within the base directory to prevent directory traversal."""
        try:
            return path.resolve().is_relative_to(self.base_directory)
        except ValueError:
            return False

    def _generate_secure_filename(self) -> str:
        """Generate a secure random filename."""
        return secrets.token_hex(16)

    def create_file(self, user_id: str, content: str) -> Optional[str]:
        """Create a new file with secure permissions."""
        if not self._is_safe_path(self.base_directory / f"{user_id}_{self._generate_secure_filename()}.txt"):
            return None
        file_path = self.base_directory / f"{user_id}_{self._generate_secure_filename()}.txt"
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
            return str(file_path)
        except IOError:
            return None

    def read_file(self, user_id: str, filename: str) -> Optional[str]:
        """Read a file if the user has permission."""
        file_path = (self.base_directory / filename).resolve()
        if not self._is_safe_path(file_path) or file_path.name != f"{user_id}_{self._generate_secure_filename()}.txt":
            return None
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except IOError:
            return None

    def delete_file(self, user_id: str, filename: str) -> bool:
        """Delete a file if the user has permission."""
        file_path = (self.base_directory / filename).resolve()
        if not self._is_safe_path(file_path) or file_path.name != f"{user_id}_{self._generate_secure_filename()}.txt":
            return False
        try:
            os.remove(file_path)
            return True
        except IOError:
            return False