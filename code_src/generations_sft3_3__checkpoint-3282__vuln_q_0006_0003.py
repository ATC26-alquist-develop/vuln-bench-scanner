import tempfile
import os

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Set restrictive permissions (only owner can read/write/execute)
        os.chmod(temp_dir, 0o700)
        
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None

# Usage
temp_folder = create_secure_temp_folder()
if temp_folder:
    print(f"Temporary directory created: {temp_folder}")
    # Use the folder...
    # Remember to clean up when done
    # os.rmdir(temp_folder)