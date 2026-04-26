import os

def read_and_write_file(file_path):
    """
    This function reads from and writes to a file efficiently.
    
    :param file_path: The path to the file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return
    
    # Check if the file is readable
    if not os.access(file_path, os.R_OK):
        print(f"The file {file_path} is not readable.")
        return
    
    # Check if the file is writable
    if not os.access(file_path, os.W_OK):
        print(f"The file {file_path} is not writable.")
        return
    
    # Read from the file
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"File content before writing: {content}")
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return
    
    # Write to the file
    try:
        with open(file_path, 'w') as file:
            file.write("This is a new content written to the file.")
            print("File content after writing: ")
            with open(file_path, 'r') as file:
                print(file.read())
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        return

# Example usage
file_path = 'example.txt'
read_and_write_file(file_path)