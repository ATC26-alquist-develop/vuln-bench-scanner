import bcrypt
import hashlib
import os

# Function to hash a password
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to check if the password is correct
def check_password(hashed_password, user_password):
    # Check if the password matches the hashed password
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Function to register a new user
def register_user(username, password):
    # Hash the password
    hashed_password = hash_password(password)
    
    # Save the username and hashed password to a file or database
    # For simplicity, we'll just print the hashed password
    print(f"Hashed Password: {hashed_password}")

    # Example: Save to a file
    # with open('users.txt', 'a') as file:
    #     file.write(f"{username}:{hashed_password}\n")

# Function to login a user
def login_user(username, password):
    # Load the hashed password from a file or database
    # For simplicity, we'll just print the hashed password
    with open('users.txt', 'r') as file:
        for line in file:
            user, hashed_password = line.strip().split(':')
            if user == username:
                if check_password(hashed_password, password):
                    print(f"Login successful for user: {username}")
                    return
                else:
                    print("Incorrect password")
                    return
        print("User not found")

# Example usage
if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    register_user(username, password)
    
    # After registration, you can prompt the user to login
    login_username = input("Enter your username for login: ")
    login_password = input("Enter your password for login: ")
    login_user(login_username, login_password)