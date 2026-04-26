def read_file(file_path):
    """Reads the content of a file and returns it."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def write_file(file_path, content):
    """Writes content to a file. If the file already exists, it will be overwritten."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
            print(f"Content written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def append_to_file(file_path, content):
    """Appends content to a file. If the file does not exist, it will be created."""
    try:
        with open(file_path, 'a') as file:
            file.write(content)
            print(f"Content appended to {file_path}")
    except Exception as e:
        print(f"An error occurred while appending to the file: {e}")

# Example usage
if __name__ == "__main__":
    file_path = 'example.txt'
    content_to_write = "Hello, this is a test."
    
    # Writing to the file
    write_file(file_path, content_to_write)
    
    # Reading from the file
    content = read_file(file_path)
    if content:
        print("File content:")
        print(content)
    
    # Appending to the file
    append_to_file(file_path, "\nThis is an appended line.")
    
    # Reading the updated file content
    updated_content = read_file(file_path)
    if updated_content:
        print("Updated file content:")
        print(updated_content)