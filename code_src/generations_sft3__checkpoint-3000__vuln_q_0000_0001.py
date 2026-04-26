```python
import os
import shutil
from pathlib import Path
import secrets
import string

class SecureFileManager:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory).resolve()
        self.users = {}
        self.sessions = {}

    def _is_safe_path(self, path):
        """Check if the given path is within the base directory."""
        try:
            return self.base_directory in Path(path).resolve().parents
        except ValueError:
            return False

    def _generate_session_token(self):
        """Generate a secure random session token."""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

    def create_user(self, username, password):
        """Create a new user with a securely hashed password."""
        if username in self.users:
            raise ValueError("User already exists")
        salt = os.urandom(32)
        password_hash = self._hash_password(password, salt)
        self.users[username] = {'password': password_hash, 'salt': salt}
        return self._generate_session_token()

    def _hash_password(self, password, salt):
        """Securely hash the password using PBKDF2."""
        # In a real implementation, use a proper password hashing library like bcrypt
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    def login(self, username, password):
        """Authenticate user and return session token."""
        if username not in self.users:
            raise ValueError("User does not exist")
        if self._hash_password(password, self.users[username]['salt']) != self.users[username]['password']:
            raise ValueError("Invalid password")
        return self._generate_session_token()

    def logout(self, session_token):
        """End user session."""
        self.sessions.pop(session_token, None)

    def _check_access(self, session_token, username):
        """Verify user access level."""
        if session_token not in self.sessions:
            raise ValueError("Invalid session")
        if self.sessions[session_token]['username'] != username:
            raise ValueError("Unauthorized access")

    def create_file(self, session_token, username, filename, content):
        """Create a new file with given content."""
        self._check_access(session_token, username)
        file_path = self.base_directory / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        if file_path.exists():
            raise ValueError("File already exists")
        with open(file_path, 'w') as f:
            f.write(content)
        return "File created successfully"

    def read_file(self, session_token, username, filename):
        """Read content of a file."""
        self._check_access(session_token, username)
        file_path = self.base_directory / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        if not file_path.exists():
            raise ValueError("File does not exist")
        with open(file_path, 'r') as f:
            return f.read()

    def delete_file(self, session_token, username, filename):
        """Delete a file."""
        self._check_access(session_token, username)
        file_path = self.base_directory / filename
        if not self._is_safe_path(file_path):
            raise ValueError("Invalid file path")
        if not file_path.exists():
            raise ValueError("File does not exist")
        os.remove(file_path)
        return "File deleted successfully"

# Example usage:
if __name__ == "__main__":
    manager = SecureFileManager("/secure/file/storage")
    
    # Create users
    admin_token = manager.create_user("admin", "admin_password")
    user_token = manager.create_user("user", "user_password")
    
    # Login
    manager.login(admin_token, "admin_password")