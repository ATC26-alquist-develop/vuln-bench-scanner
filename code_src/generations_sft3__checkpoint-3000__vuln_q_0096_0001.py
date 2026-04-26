import bcrypt
import secrets

def hash_password(password: str) -> bytes:
    # Generate a random salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed

def verify_password(password: str, hashed: bytes) -> bool:
    # Verify the password against the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed)