# Basic User Authentication System


# Simulated user database

users = {

    'user1': 'password123',

    'user2': 'mypassword',

    'admin': 'adminpass'

}


def authenticate(username, password):

    if username in users and users[username] == password:

        return True

    return False


# Simulate user login

username_input = input("Enter username: ")

password_input = input("Enter password: ")

if authenticate(username_input, password_input):

    print("Login successful!")

else:

    print("Invalid username or password!")


# End of script