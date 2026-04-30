import bcrypt

def hash_password(password: str) -> bytes:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password: str, hashed: bytes) -> bool:
    # Verify the password against the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed)