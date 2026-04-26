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
        except (ValueError, RuntimeError):
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

    def _hash_password(self, password, salt):
        """Securely hash the password using PBKDF2."""
        # In a real-world scenario, use a proper password hashing library like bcrypt
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    def login(self, username, password):
        """Authenticate user and create session."""
        if username not in self.users:
            raise ValueError("User does not exist")
        user = self.users[username]
        if self._hash_password(password, user['salt']) != user['password']:
            raise ValueError("Invalid password")
        
        session_token = self._generate_session_token()
        self.sessions[session_token] = username
        return session_token

    def logout(self, session_token):
        """End user session."""
        if session_token in self.sessions:
            del self.sessions[session_token]

    def create_file(self, session_token, filename, content):
        """Create a new file with the given content."""
        if not self._is_safe_path(filename):
            raise ValueError("Invalid file path")
        
        if not self._is_allowed(session_token, filename, 'create'):
            raise PermissionError("Access denied")
        
        file_path = self.base_directory / filename
        if file_path.exists():
            raise FileExistsError("File already exists")
        
        with open(file_path, 'w') as f:
            f.write(content)

    def read_file(self, session_token, filename):
        """Read the contents of a file."""
        if not self._is_safe_path(filename):
            raise ValueError("Invalid file path")
        
        if not self._is_allowed(session_token, filename, 'read'):
            raise PermissionError("Access denied")
        
        file_path = self.base_directory / filename
        if not file_path.exists():
            raise FileNotFoundError("File not found")
        
        with open(file_path, 'r') as f:
            return f.read()

    def delete_file(self, session_token, filename):
        """Delete a file."""
        if not self._is_safe_path(filename):
            raise ValueError("Invalid file path")
        
        if not self._is_allowed(session_token, filename, 'delete'):
            raise PermissionError("Access denied")
        
        file_path = self.base_directory / filename
        if not file_path.exists():
            raise FileNotFoundError("File not found")
        
        os.remove(file_path)

    def _is_allowed(self, session_token, filename, action):
        """Check if the user has permission for the requested action."""
        if session_token not in self.sessions:
            return False
        
        username = self.sessions[session_token]
        # Default deny
        allowed = False
        
        # Implement your access control logic here
        # For example, allow all users to