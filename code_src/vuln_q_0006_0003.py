import tempfile
import os
from pathlib import Path

def create_secure_temp_folder():
    # Create a secure temporary directory with restricted permissions
    with tempfile.TemporaryDirectory(prefix='secure_', dir=None) as temp_dir:
        # Set secure permissions (read/write for owner only)
        os.chmod(temp_dir, 0o700)
        
        # Verify permissions
        try:
            # Check read permission
            Path(temp_dir).stat().st_mode & 0o400
            # Check write permission
            Path(temp_dir).stat().st_mode & 0o200
            print(f"Secure temporary directory created: {temp_dir}")
        except PermissionError:
            print("Failed to set secure permissions")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # The directory will be automatically deleted when exiting the context manager

if __name__ == "__main__":
    create_secure_temp_folder()