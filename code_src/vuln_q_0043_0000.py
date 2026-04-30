```python
import bcrypt
import secrets
import re
from typing import Optional
import sqlite3
from contextlib import contextmanager

class SecureUserRegistration:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _init_db(self):
        """Secure database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            conn.commit()
            yield cursor
        finally:
            conn.close()

    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return (len(password) >= 12 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)

    def register_user(self, username: str, password: str) -> bool:
        """Register new user with secure password hashing"""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        try:
            with self._init_db() as cursor:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed_password)
                )
                self._init_db().commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
        except Exception:
            return False  # Log error securely

    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        try:
            with self._init_db() as cursor:
                cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                if result:
                    stored_hash = result[0]
                    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
            return False
        except Exception:
            return False  # Log error securely
```