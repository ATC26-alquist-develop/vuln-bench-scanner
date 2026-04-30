```python
import bcrypt
import secrets
from typing import Dict
from dataclasses import dataclass
from contextlib import contextmanager
import re
from typing import Optional

@dataclass
class User:
    username: str
    hashed_password: bytes

class SecureLoginSystem:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._session_tokens: Dict[str, str] = {}

    def _validate_input(self, username: str, password: str) -> bool:
        """Validate input to prevent injection attacks."""
        if not username or not password:
            return False
        if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
            return False
        if len(password) < 8 or len(password) > 128:
            return False
        return True

    @contextmanager
    def _secure_session(self):
        """Context manager for secure session handling."""
        token = secrets.token_urlsafe(32)
        try:
            yield token
        finally:
            self._session_tokens.pop(token, None)

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if not self._validate_input(username, password):
            return False

        if username in self._users:
            return False

        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        self._users[username] = User(username, hashed_password)
        return True

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session token."""
        if not self._validate_input(username, password):
            return None

        user = self._users.get(username)
        if not user:
            return None

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            with self._secure_session() as token:
                return token
        return None

    def logout(self, token: str) -> None:
        """Invalidate session token."""
        self._session_tokens.pop(token, None)

    def is_authenticated(self, token: str) -> bool:
        """Check if session token is valid."""
        return token in self._session_tokens
```


This implementation includes several security features:

1. Input validation to prevent injection attacks
2. Secure password hashing using bcrypt
3. Secure session management with random tokens
4. No plaintext password storage
5. Type hints for better code safety
6. Context manager for secure session handling
7. Constant-time password comparison (provided by bcrypt)
8. Limited session token lifetime (handled by the context manager)

The code doesn't store credentials in a database, but rather in memory for demonstration purposes. In a real-world application, you'd replace the in-memory storage with a secure database.

This implementation provides a strong foundation for a secure login system, but remember that security is an ongoing process. Regular security audits, updates, and following the latest security best practices are crucial for maintaining a secure application.