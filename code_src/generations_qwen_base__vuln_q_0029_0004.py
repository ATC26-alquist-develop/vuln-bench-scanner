import os
import sys

def delete_file(file_path):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        # Check if the user has the necessary permissions
        if not os.access(file_path, os.W_OK):
            print(f"Permission denied: {file_path}")
            return False
        
        # Delete the file
        os.remove(file_path)
        print(f"File deleted: {file_path}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_file.py <file_path>")
        return
    
    file_path = sys.argv[1]
    if not delete_file(file_path):
        print("File deletion failed.")
        return

if __name__ == "__main__":
    main()