import datetime


# A simple dictionary to store user credentials and login history

user_credentials = {

    'user1': 'password123',

    'user2': 'mypassword'

}


# A dictionary to store login history

login_history = {}


def authenticate(username, password):

    if username in user_credentials and user_credentials[username] == password:

        # Log the successful login with a timestamp

        login_history[username] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Login successful for {username}.")

        return True

    else:

        print("Invalid username or password.")

        return False


# Example usage:

username_input = input("Enter username: ")

password_input = input("Enter password: ")

authenticate(username_input, password_input)


# Print login history

print("\nLogin History:")

for user, timestamp in login_history.items():

    print(f"{user}: {timestamp}")