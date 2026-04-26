import os
import getpass

class FileManager:
    def __init__(self):
        self.files = {}
        self.users = {}
        self.current_user = None

    def register_user(self, username, password):
        if username not in self.users:
            self.users[username] = password
            print(f"User {username} registered successfully.")
        else:
            print(f"User {username} already exists.")

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            print(f"Logged in as {username}.")
        else:
            print("Invalid username or password.")

    def create_file(self, filename):
        if self.current_user:
            if filename not in self.files:
                with open(filename, 'w'):
                    pass
                self.files[filename] = {'created_by': self.current_user}
                print(f"File {filename} created successfully.")
            else:
                print(f"File {filename} already exists.")
        else:
            print("You must be logged in to create a file.")

    def delete_file(self, filename):
        if self.current_user:
            if filename in self.files:
                del self.files[filename]
                os.remove(filename)
                print(f"File {filename} deleted successfully.")
            else:
                print(f"File {filename} does not exist.")
        else:
            print("You must be logged in to delete a file.")

    def view_files(self):
        if self.current_user:
            if self.files:
                print("Files:")
                for filename, details in self.files.items():
                    print(f"  {filename} (Created by: {details['created_by']})")
            else:
                print("No files found.")
        else:
            print("You must be logged in to view files.")

def main():
    file_manager = FileManager()
    
    while True:
        print("\nFile Management System")
        print("1. Register User")
        print("2. Login")
        print("3. Create File")
        print("4. Delete File")
        print("5. View Files")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            file_manager.register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            file_manager.login(username, password)
        elif choice == '3':
            if file_manager.current_user:
                filename = input("Enter filename: ")
                file_manager.create_file(filename)
            else:
                print("You must be logged in to create a file.")
        elif choice == '4':
            if file_manager.current_user:
                filename = input("Enter filename: ")
                file_manager.delete_file(filename)
            else:
                print("You must be logged in to delete a file.")
        elif choice == '5':
            if file_manager.current_user:
                file_manager.view_files()
            else:
                print("You must be logged in to view files.")
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()