import tempfile
import os

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        with tempfile.TemporaryDirectory(prefix='secure_') as temp_dir:
            # Set restrictive permissions (only owner can read/write)
            os.chmod(temp_dir, 0o700)
            
            # Use the temporary directory
            with open(os.path.join(temp_dir, 'test.txt'), 'w') as f:
                f.write('Hello, secure world!')
                
            # The directory will be automatically deleted when exiting the context manager
            return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None