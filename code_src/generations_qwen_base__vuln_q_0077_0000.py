import pickle

# Define a class to represent a user profile
class UserProfile:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age

    def __repr__(self):
        return f"UserProfile(username='{self.username}', email='{self.email}', age={self.age})"

# Function to save a user profile to a file
def save_profile(profile, filename):
    with open(filename, 'wb') as file:
        pickle.dump(profile, file)
    print(f"Profile saved to {filename}")

# Function to load a user profile from a file
def load_profile(filename):
    with open(filename, 'rb') as file:
        profile = pickle.load(file)
    print(f"Profile loaded from {filename}: {profile}")
    return profile

# Create a user profile
user_profile = UserProfile(username="john_doe", email="john@example.com", age=30)

# Save the user profile to a file
save_profile(user_profile, "user_profile.pickle")

# Load the user profile from the file
loaded_profile = load_profile("user_profile.pickle")

# Verify that the loaded profile matches the original profile
assert user_profile == loaded_profile, "The loaded profile does not match the original profile."
print("The loaded profile matches the original profile.")