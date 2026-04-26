import os
import tempfile

def create_temp_directory():
    # Create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_dir_path = temp_dir.name

    # Get the current user ID
    current_user_id = os.getuid()

    # Set the permissions for the directory
    os.chmod(temp_dir_path, 0o777)  # 0o777 is the octal representation of 777 (rwxrwxrwx)

    # Print the path of the created directory
    print(f"Temporary directory created at: {temp_dir_path}")

    return temp_dir_path

# Create the temporary directory
temp_dir_path = create_temp_directory()