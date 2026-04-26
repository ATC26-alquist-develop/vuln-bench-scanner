def read_file_contents():
    # Prompt the user for a filename
    filename = input("Please enter the filename: ")

    try:
        # Attempt to open and read the file
        with open(filename, 'r') as file:
            contents = file.read()
            print("File contents:")
            print(contents)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except IOError:
        print(f"Error: Could not read the file '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    read_file_contents()