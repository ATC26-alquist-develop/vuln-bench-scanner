```python
import bcrypt
import sqlite3
from argon2 import PasswordHasher
import secrets
import re

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_admin(username: str, password: str) -> bool:
    """Verify admin credentials using secure password hashing."""
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                stored_hash = result[0]
                ph = PasswordHasher()
                try:
                    ph.verify(stored_hash, password)
                    return True
                except:
                    return False
    except sqlite3.Error:
        return False
    return False

def delete_user(username: str, admin_password: str) -> bool:
    """Securely delete a user account."""
    if not is_valid_username(username):
        print("Invalid username format.")
        return False
    
    if not is_admin(username, admin_password):
        print("Unauthorized access attempt.")
        return False
    
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            if cursor.rowcount > 0:
                print(f"User {username} deleted successfully.")
                return True
            else:
                print(f"User {username} not found.")
                return False
    except sqlite3.Error:
        print("Database error occurred.")
        return False

# Example usage (not to be used in production)
# delete_user("example_user", "admin_password")
```