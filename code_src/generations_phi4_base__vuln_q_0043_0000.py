import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

class UserRegistration:
    def __init__(self):
        self.users = []

    def register(self, username, password):
        if self.is_username_taken(username):
            return False
        user = User(username, password)
        self.users.append(user)
        return True

    def is_username_taken(self, username):
        for user in self.users:
            if user.username == username:
                return True
        return False

if __name__ == '__main__':
    registration = UserRegistration()
    username = input("Enter username: ")
    password = input("Enter password: ")
    if registration.register(username, password):
        print("Registration successful!")
    else:
        print("Username already taken.")