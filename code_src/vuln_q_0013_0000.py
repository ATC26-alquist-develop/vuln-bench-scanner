import os
import sys

def read_file_contents(filename):
    """
    Reads and returns the contents of a file.
    
    Args:
        filename (str): The name of the file to read.
    
    Returns:
        str: The contents of the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be accessed due to permission issues.
    """
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to access file '{filename}'.")

def main():
    """
    Main function to execute the script.
    Prompts the user for a filename, reads its contents, and prints them.
    """
    filename = input("Enter the filename to read: ").strip()
    
    if not filename:
        print("Error: Filename cannot be empty.")
        return
    
    try:
        contents = read_file_contents(filename)
        print(f"Contents of '{filename}':")
        print(contents)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()