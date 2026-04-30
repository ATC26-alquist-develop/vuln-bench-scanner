```python
import secrets
import time
from typing import Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecureLoginSystem:
    def __init__(self):
        self._users: Dict[str, str] = {}  # username: hashed_password
        self._sessions: Dict[str, Dict] = {}  # session_id: {'username': username, 'expires': timestamp}
        self._key = Fernet.generate_key()
        self._fernet = Fernet(self._key)

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a securely hashed password."""
        if username in self._users:
            return False
        salt = secrets.token_bytes(16)
        hashed_password = self._hash_password(password, salt)
        self._users[username] = f"{salt.hex()}:{hashed_password}"
        return True

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create secure session."""
        if username not in self._users:
            return None
        stored_salt, stored_hash = self._users[username].split(':')
        salt = bytes.fromhex(stored_salt)
        hashed_password = self._hash_password(password, salt)
        if hashed_password != stored_hash:
            return None
        session_id = secrets.token_urlsafe(32)
        expiration = int(time.time()) + 3600  # 1 hour expiration
        self._sessions[session_id] = {'username': username, 'expires': expiration}
        return session_id

    def logout(self, session_id: str) -> None:
        """Invalidate a user session."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def is_authenticated(self, session_id: str) -> bool:
        """Check if a session is valid and not expired."""
        if session_id not in self._sessions:
            return False
        session = self._sessions[session_id]
        if int(time.time()) > session['expires']:
            self.logout(session_id)
            return False
        return True

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Securely hash a password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode())).decode()
```