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
        
    def create_user(self, username, password):
        if username in self.users:
            raise ValueError("User already exists")
        salt = secrets.token_bytes(16)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = {'password': hashed_password, 'salt': salt}
        return self._create_session(username)
    
    def _hash_password(self, password, salt):
        # In a real system, use a secure hashing algorithm like bcrypt
        return hash(password + salt.hex())
    
    def _create_session(self, username):
        session_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        self.sessions[session_id] = username
        return session_id
    
    def _verify_session(self, session_id):
        if session_id not in self.sessions:
            raise ValueError("Invalid session")
    
    def _get_user_path(self, session_id):
        username = self.sessions[session_id]
        return self.base_directory / username
    
    def _is_safe_path(self, path):
        try:
            return path.resolve().parent == self.base_directory
        except (ValueError, RuntimeError):
            return False
    
    def view_file(self, session_id, filename):
        self._verify_session(session_id)
        user_path = self._get_user_path(session_id)
        file_path = user_path / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Access denied")
            
        if not file_path.is_file():
            raise FileNotFoundError("File not found")
            
        with open(file_path, 'r') as f:
            return f.read()
    
    def create_file(self, session_id, filename, content):
        self._verify_session(session_id)
        user_path = self._get_user_path(session_id)
        file_path = user_path / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Access denied")
            
        with open(file_path, 'w') as f:
            f.write(content)
    
    def delete_file(self, session_id, filename):
        self._verify_session(session_id)
        user_path = self._get_user_path(session_id)
        file_path = user_path / filename
        
        if not self._is_safe_path(file_path):
            raise ValueError("Access denied")
            
        if not file_path.is_file():
            raise FileNotFoundError("File not found")
            
        file_path.unlink()