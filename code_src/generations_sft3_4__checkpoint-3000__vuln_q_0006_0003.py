import tempfile
import os

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"Created temporary directory: {temp_dir}")
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None

# Usage
temp_folder = create_secure_temp_folder()
if temp_folder:
    try:
        # Perform operations with the temporary folder
        os.rmdir(temp_folder)
    except Exception as e:
        print(f"Error removing temporary directory: {e}")