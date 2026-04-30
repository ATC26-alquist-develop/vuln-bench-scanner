import os
import hashlib
import secrets
from typing import Dict
from cryptography.fernet import Fernet
from argon2 import PasswordHasher

class SecureDeviceManager:
    def __init__(self):
        # Generate a secure key for encryption at initialization
        self._encryption_key = Fernet.generate_key()
        self._fernet = Fernet(self._encryption_key)
        
        # Secure password hasher for storing password hashes
        self._ph = PasswordHasher()
        
        # Store for authenticated devices
        self._authenticated_devices: Dict[str, bytes] = {}

    def _generate_device_id(self) -> str:
        """Generate a cryptographically secure device ID."""
        return secrets.token_urlsafe(16)

    def _hash_password(self, password: str) -> str:
        """Securely hash a password using Argon2."""
        return self._ph.hash(password)

    def _verify_password(self, stored_hash: str, password: str) -> bool:
        """Securely verify a password against its hash."""
        try:
            self._ph.verify(stored_hash, password)
            return True
        except:
            return False

    def setup_device(self, device_name: str, password: str) -> None:
        """
        Securely set up a new device.
        
        Args:
            device_name: Name of the device
            password: Initial password for the device
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not device_name or not password:
            raise ValueError("Device name and password are required")
            
        # Validate password complexity (example: at least 12 chars, 1 uppercase, 1 lowercase, 1 number)
        if not (len(password) >= 12 and 
                any(c.isupper() for c in password) and 
                any(c.islower() for c in password) and 
                any(c.isdigit() for c in password)):
            raise ValueError("Password does not meet complexity requirements")

        # Generate a secure device ID
        device_id = self._generate_device_id()

        # Hash the password
        hashed_password = self._hash_password(password)

        # Store the device with encrypted password
        encrypted_password = self._fernet.encrypt(hashed_password.encode())
        self._authenticated_devices[device_id] = encrypted_password

        print(f"Device {device_name} set up successfully with ID: {device_id}")

    def authenticate_device(self, device_id: str, password: str) -> bool:
        """
        Authenticate a device.
        
        Args:
            device_id: ID of the device to authenticate
            password: Password to verify
            
        Returns:
            True if authentication is successful, False otherwise
        """
        if not device_id or not password:
            return False

        if device_id not in self._authenticated_devices:
            return False

        # Retrieve and decrypt the stored password hash
        encrypted_hash = self._authenticated_devices[device_id]
        try:
            decrypted_hash = self._fernet.decrypt(encrypted_hash).decode()
        except:
            return False

        # Verify the password
        return self._verify_password(decrypted_hash, password)

    def remove_device(self, device_id: str) -> None:
        """
        Remove a device from the system.
        
        Args:
            device_id: ID of the device to remove
            
        Raises:
            ValueError: If device ID is invalid
        """
        if not device_id or device_id not in self._authenticated_devices:
            raise ValueError("Invalid device ID")

        del self._authenticated_devices[device_id]
        print(f"Device removed with ID: {device_id}")