import tempfile

def create_secure_temp_folder():
    try:
        # Create a secure temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"Temporary directory created: {temp_dir}")
        return temp_dir
    except Exception as e:
        print(f"Error creating temporary directory: {e}")
        return None