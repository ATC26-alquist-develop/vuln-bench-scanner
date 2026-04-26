import tempfile
import os

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"Secure temporary directory created: {temp_dir}")
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None