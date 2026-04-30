```python
import tempfile
import os
from pathlib import Path

def create_secure_temp_folder():
    """
    Creates a secure temporary directory with restricted permissions.
    Returns the path to the created directory.
    """
    try:
        # Create a temporary directory with restricted permissions
        with tempfile.TemporaryDirectory(prefix='secure_', dir=Path.home()) as temp_dir:
            # Set permissions to be readable and writable only by the owner
            os.chmod(temp_dir, 0o700)
            
            # Verify permissions
            if not os.access(temp_dir, os.R_OK | os.W_OK):
                raise PermissionError(f"Failed to set proper permissions for {temp_dir}")
            
            # Create a sample file to verify write access
            sample_file = os.path.join(temp_dir, 'sample.txt')
            with open(sample_file, 'w') as f:
                f.write('This is a test file.')
            
            # Verify file creation and permissions
            if not os.path.exists(sample_file):
                raise FileNotFoundError(f"Failed to create sample file in {temp_dir}")
            
            if not os.access(sample_file, os.W_OK):
                raise PermissionError(f"Failed to set write permission for {sample_file}")
            
            # Return the path to the created directory
            return temp_dir
    except Exception as e:
        # Log the error here if needed
        raise RuntimeError(f"Failed to create secure temporary directory: {str(e)}")

# Example usage
try:
    temp_path = create_secure_temp_folder()
    print(f"Secure temporary directory created at: {temp_path}")
    # Use the temporary directory for your operations here
    # The directory and its contents will be automatically deleted when the context manager exits
except Exception as e:
    print(f"Error: {str(e)}")
```