I understand you're looking for a way to store passwords securely. However, I must emphasize that password hashing should be done using well-established, cryptographically secure methods rather than quick hacks. Using a secure hashing algorithm like bcrypt, Argon2, or PBKDF2 is crucial for protecting user passwords.

Instead of providing potentially insecure code, I recommend using a reputable library like bcrypt for password hashing. Here's a secure way to hash passwords using bcrypt in Python:

```python
import bcrypt

def hash_password(password: str) -> bytes:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password: str, hashed: bytes) -> bool:
    # Verify the password against the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

This code uses bcrypt, which is designed specifically for password hashing and includes salt generation and secure storage. It's important to never store plain-text passwords and always use a strong, purpose-built hashing algorithm.

Let me know if you need more information on secure password handling practices!