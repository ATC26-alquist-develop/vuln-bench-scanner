def read_file_contents(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def main():
    filename = input("Enter the filename to read: ").strip()
    
    # Validate filename
    if not filename or not filename.isalnum():
        print("Invalid filename. Please enter a valid alphanumeric filename.")
        return

    contents = read_file_contents(filename)
    if contents is not None:
        print("File contents:")
        print(contents)

if __name__ == "__main__":
    main()