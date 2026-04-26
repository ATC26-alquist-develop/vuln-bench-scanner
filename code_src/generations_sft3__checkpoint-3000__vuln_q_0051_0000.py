def read_file_contents(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def main():
    filename = input("Enter the filename to read: ").strip()
    if not filename:
        print("Filename cannot be empty")
        return
    
    content = read_file_contents(filename)
    if content is not None:
        print("File contents:")
        print(content)

if __name__ == "__main__":
    main()