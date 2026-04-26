import json
import os
from typing import Dict, Any

class UserProfile:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(username=data['username'], email=data['email'])

def save_user_profile(profile: UserProfile, filename: str) -> None:
    """Safely save user profile to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile.to_dict(), f, indent=2)
    except IOError as e:
        print(f"Error saving profile: {e}")

def load_user_profile(filename: str) -> UserProfile:
    """Safely load user profile from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return UserProfile.from_dict(data)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading profile: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Create and save profile
    profile = UserProfile(username="john_doe", email="john@example.com")
    save_user_profile(profile, "user_profile.json")
    
    # Load profile
    loaded_profile = load_user_profile("user_profile.json")
    if loaded_profile:
        print(f"Loaded profile: {loaded_profile.username}, {loaded_profile.email}")