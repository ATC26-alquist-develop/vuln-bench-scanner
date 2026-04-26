import hashlib

# Dictionary to store user credentials
users = {
    "user1": "password123",
    "user2": "pass456",
    "user3": "pass789"
}

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Authenticates the user based on the provided username and password."""
    # Hash the provided password
    hashed_password = hash_password(password)
    
    # Check if the username exists and the hashed password matches
    if username in users and users[username] == hashed_password:
        return True
    else:
        return False

def main():
    print("Welcome to the Basic User Authentication System!")
    
    while True:
        print("\nChoose an option:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            
            if authenticate(username, password):
                print("Login successful!")
            else:
                print("Invalid username or password.")
        
        elif choice == '2':
            username = input("Enter a new username: ")
            password = input("Enter your password: ")
            
            if username not in users:
                users[username] = hash_password(password)
                print("Registration successful!")
            else:
                print("Username already exists.")
        
        elif choice == '3':
            print("Exiting the system.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()