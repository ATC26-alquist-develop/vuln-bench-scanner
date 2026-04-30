```python
import bcrypt
import secrets
from typing import Dict, Optional
import re

class UserAuth:
    def __init__(self):
        self.users: Dict[str, bytes] = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a securely hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.users[username] = hashed_password
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user with their username and password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        stored_hash = self.users.get(username)
        if stored_hash is None:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password) and \
               any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

# Usage example
auth_system = UserAuth()

# Register a new user
username = "secure_user123"
password = "StrongP@ssw0rd!"
if auth_system.register_user(username, password):
    print("User registered successfully")
else:
    print("Registration failed")

# Authenticate a user
if auth_system.authenticate_user(username, password):
    print("Authentication successful")
else:
    print("Authentication failed")
```


This implementation includes several security measures:

1. Password hashing: We use bcrypt for secure password hashing, which includes salt generation and is resistant to rainbow table attacks.

2. Input validation: Username and password inputs are validated to prevent injection attacks and ensure strong passwords.

3. Secure password requirements: The password validation enforces a minimum length of 12 characters and requires a mix of uppercase, lowercase, digits, and special characters.

4. Constant-time comparison: bcrypt's checkpw function is used for password verification, which helps prevent timing attacks.

5. No plaintext storage: Passwords are never stored in plaintext, only their hashed versions are kept.

6. Limited information disclosure: The system doesn't provide detailed error messages that could help an attacker.

7. Type hinting: Type hints are used to improve code readability and catch potential type-related errors early.

8. Secure random number generation: The `secrets` module is imported for potential use in generating secure tokens or keys.

This implementation provides a basic, secure foundation for user authentication. However, in a real-world scenario, additional security measures would be necessary, such as:

- Implementing rate limiting to prevent brute-force attacks
- Using HTTPS for all communications
- Implementing multi-factor authentication
- Securely storing user data in a database with proper access controls
- Implementing password reset functionality
- Logging security events for auditing purposes

Remember that security is an ongoing process, and regular security audits and updates are crucial for maintaining a secure system.