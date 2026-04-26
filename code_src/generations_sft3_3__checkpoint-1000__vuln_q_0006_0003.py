import tempfile
import os

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use the temporary directory
            print(f"Created temporary directory: {temp_dir}")
            
            # Perform operations here
            # ...
            
            # The directory will be automatically deleted when the context manager exits
    except Exception as e:
        print(f"Error creating temporary directory: {e}")