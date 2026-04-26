import tempfile
import os

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        temp_dir = tempfile.mkdtemp(prefix='secure_')
        
        # Set restrictive permissions (700)
        os.chmod(temp_dir, 0o700)
        
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None