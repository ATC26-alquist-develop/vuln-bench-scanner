import bcrypt
import secrets
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users: Dict[str, bytes] = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a securely hashed password."""
        if not username or not password:
            return False
        
        if username in self.users:
            return False  # User already exists
        
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Store the hashed password
        self.users[username] = hashed_password
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user by comparing the provided password with the stored hash."""
        if not username or not password:
            return False
        
        stored_hash = self.users.get(username)
        if not stored_hash:
            return False  # User not found
        
        # Use constant-time comparison to prevent timing attacks
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change a user's password after verifying the old password."""
        if not username or not old_password or not new_password:
            return False
        
        if not self.authenticate_user(username, old_password):
            return False  # Old password is incorrect
        
        # Generate a new salt and hash the new password
        salt = bcrypt.gensalt()
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        
        # Update the stored password
        self.users[username] = new_hashed_password
        return True

    def generate_reset_token(self, username: str) -> Optional[str]:
        """Generate a secure token for password reset (placeholder implementation)."""
        if not username:
            return None
        
        # In a real implementation, use a secure random token generation
        # and store it in a separate, secure database with an expiration time
        return secrets.token_urlsafe(32)

# Example usage:
auth_system = UserAuth()

# Register a new user
auth_system.register_user("alice", "securepassword123")

# Authenticate a user
is_authenticated = auth_system.authenticate_user("alice", "securepassword123")
print(f"Authentication successful: {is_authenticated}")

# Change password
auth_system.change_password("alice", "securepassword123", "newSecurePassword456")

# Generate reset token (placeholder)
reset_token = auth_system.generate_reset_token("alice")
print(f"Reset token: {reset_token}")