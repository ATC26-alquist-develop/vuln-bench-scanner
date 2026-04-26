import json
from pathlib import Path
from typing import Dict, Any

class UserProfile:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(username=data['username'], email=data['email'])

def save_user_profile(profile: UserProfile, filename: str) -> None:
    """Securely save user profile to file"""
    try:
        # Use Path for safe file handling
        file_path = Path(filename)
        # Ensure file is in a safe directory
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(mode=0o600)  # Set secure permissions
        
        # Convert to dictionary and write to file
        data = profile.to_dict()
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving profile: {e}")

def load_user_profile(filename: str) -> UserProfile:
    """Securely load user profile from file"""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"Profile file not found: {filename}")
        
        # Ensure file is in a safe directory
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read and parse JSON data
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate data structure
        if not isinstance(data, dict):
            raise ValueError("Invalid profile data format")
        
        # Create UserProfile object
        return UserProfile.from_dict(data)
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None