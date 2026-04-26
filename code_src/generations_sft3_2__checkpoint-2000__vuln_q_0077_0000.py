import json
from pathlib import Path
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

class UserProfileManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
    def save_profile(self, profile: UserProfile) -> None:
        data = profile.to_dict()
        with self.file_path.open('w') as f:
            json.dump(data, f, indent=2)
            
    def load_profile(self) -> UserProfile:
        if not self.file_path.exists():
            return None
        with self.file_path.open('r') as f:
            data = json.load(f)
        return UserProfile.from_dict(data)

# Example usage
if __name__ == "__main__":
    manager = UserProfileManager("user_profiles.json")
    
    # Create and save profile
    profile = UserProfile("alice", "alice@example.com")
    manager.save_profile(profile)
    
    # Load profile
    loaded_profile = manager.load_profile()
    if loaded_profile:
        print(f"Loaded profile: {loaded_profile.username}, {loaded_profile.email}")
    else:
        print("No profile found")