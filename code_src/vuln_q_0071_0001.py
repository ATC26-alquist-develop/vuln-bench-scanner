from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass
from html import escape
import bcrypt
import secrets
import sqlite3
from contextlib import contextmanager
import re

@dataclass
class Message:
    """Secure message structure with validation"""
    content: str
    author: str
    timestamp: datetime
    _id: int = None

class SecureForum:
    def __init__(self, db_path: str):
        """Initialize forum with secure database connection"""
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Create database with secure schema"""
        with self._get_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    author TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    @contextmanager
    def _get_db_connection(self):
        """Secure database connection context manager"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        finally:
            if conn:
                conn.close()

    def _validate_input(self, content: str) -> bool:
        """Validate input to prevent injection attacks"""
        if not content or len(content) > 1000:  # Reasonable length limit
            return False
        # Remove any potentially dangerous characters
        content = re.sub(r'[^\w\s.,!?-]', '', content)
        return True

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing"""
        if not self._validate_input(username) or not self._validate_input(password):
            return False

        password_hash = bcrypt.hashpw(password.encode('utf-8'), 
                                      bcrypt.gensalt(rounds=12))  # Strong hashing

        try:
            with self._get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def login_user(self, username: str, password: str) -> bool:
        """Securely verify user credentials"""
        if not self._validate_input(username) or not self._validate_input(password):
            return False

        try:
            with self._get_db_connection() as conn:
                cursor = conn.execute(
                    "SELECT password_hash FROM users WHERE username = ?",
                    (username,)
                )
                result = cursor.fetchone()
                if result:
                    stored_hash = result[0]
                    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except sqlite3.Error:
            pass
        return False

    def post_message(self, user: str, content: str) -> bool:
        """Securely post a message"""
        if not self._validate_input(content):
            return False

        message = Message(
            content=content,
            author=user,
            timestamp=datetime.now()
        )

        try:
            with self._get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO messages (content, author) VALUES (?, ?)",
                    (message.content, message.author)
                )
            return True
        except sqlite3.Error:
            return False

    def get_messages(self) -> List[Message]:
        """Securely retrieve messages"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.execute(
                    "SELECT content, author, timestamp FROM