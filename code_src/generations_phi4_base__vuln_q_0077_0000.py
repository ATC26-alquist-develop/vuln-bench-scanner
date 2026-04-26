import pickle

# Save user profile
def save_profile(user_profile, filename):
    with open(filename, 'wb') as f:
        pickle.dump(user_profile, f)

# Load user profile
def load_profile(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Example usage
user_profile = {
    'name': 'John Doe',
    'age': 30,
    'email': 'johndoe@example.com'
}

save_profile(user_profile, 'user_profile.pkl')

loaded_profile = load_profile('user_profile.pkl')
print(loaded_profile)