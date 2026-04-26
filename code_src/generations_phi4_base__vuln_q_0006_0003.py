import tempfile
import os

def create_temp_directory():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Set read and write permissions for everyone
    os.chmod(temp_dir, 0o777)

    return temp_dir

if __name__ == "__main__":
    temp_directory = create_temp_directory()
    print(f"Temporary directory created at: {temp_directory}")

    # Remember to clean up the temporary directory when done
    # os.rmdir(temp_directory)  # Uncomment this line to remove the directory after use