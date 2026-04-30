I can help you with secure password hashing, but it's important to use well-established, cryptographically secure methods rather than implementing custom solutions. For password hashing, I recommend using bcrypt or Argon2. Here's an example using bcrypt:

```python
import bcrypt

def hash_password(password: str) -> bytes:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

This uses bcrypt, which is designed for password hashing and includes salt generation and secure storage. It's much safer than implementing your own solution. Let me know if you need more details!