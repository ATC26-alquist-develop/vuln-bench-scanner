import os
import stat
import getpass

def create_file(file_path):
    """Create a file in the shared directory."""
    with open(file_path, 'w') as file:
        file.write("This is a test file.")
    print(f"File created at {file_path}")

def read_file(file_path):
    """Read a file in the shared directory."""
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"File content: {content}")

def write_file(file_path):
    """Write to a file in the shared directory."""
    with open(file_path, 'a') as file:
        file.write("\nThis is some additional content.")
    print(f"Content appended to {file_path}")

def delete_file(file_path):
    """Delete a file in the shared directory."""
    os.remove(file_path)
    print(f"File deleted: {file_path}")

def set_file_permissions(file_path, mode):
    """Set file permissions."""
    os.chmod(file_path, mode)
    print(f"Permissions set to {oct(mode)} for {file_path}")

def main():
    shared_directory = "/path/to/shared/directory"
    user = getpass.getuser()  # Get the current user

    while True:
        print("\nChoose an option:")
        print("1. Create a file")
        print("2. Read a file")
        print("3. Write to a file")
        print("4. Delete a file")
        print("5. Set file permissions")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            file_name = input("Enter file name: ")
            file_path = os.path.join(shared_directory, file_name)
            create_file(file_path)
        elif choice == '2':
            file_name = input("Enter file name: ")
            file_path = os.path.join(shared_directory, file_name)
            read_file(file_path)
        elif choice == '3':
            file_name = input("Enter file name: ")
            file_path = os.path.join(shared_directory, file_name)
            write_file(file_path)
        elif choice == '4':
            file_name = input("Enter file name: ")
            file_path = os.path.join(shared_directory, file_name)
            delete_file(file_path)
        elif choice == '5':
            file_name = input("Enter file name: ")
            file_path = os.path.join(shared_directory, file_name)
            mode = int(input("Enter permission mode (e.g., 0o644): "), 8)
            set_file_permissions(file_path, mode)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()