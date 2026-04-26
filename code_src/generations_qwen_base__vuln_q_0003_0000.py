import os
import datetime

# Dictionary to store user credentials
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

# Function to check if the user credentials are correct
def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Function to log the login event
def log_login(username):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("login_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - {username} logged in successfully.\n")

# Main authentication loop
def main():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if authenticate(username, password):
            print("Login successful!")
            log_login(username)
            break
        else:
            print("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()