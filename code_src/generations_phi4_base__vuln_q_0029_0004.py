import os

def list_files(directory):
    """List all files in the given directory."""
    try:
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return []

def delete_file(file_path):
    """Delete a file at the specified path."""
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    else:
        print(f"The file '{file_path}' does not exist.")

def main():
    while True:
        print("\nFile Management Tool")
        print("1. List Files")
        print("2. Delete File")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            directory = input("Enter the directory path: ")
            files = list_files(directory)
            if files:
                print("Files in directory:")
                for file in files:
                    print(file)
            else:
                print("No files found in the directory.")

        elif choice == '2':
            file_path = input("Enter the full path of the file to delete: ")
            delete_file(file_path)

        elif choice == '3':
            print("Exiting the tool.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()