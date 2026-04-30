import os
import secrets
import hashlib

# Predefined list of allowed file paths (whitelist)
ALLOWED_FILES = {
    '/path/to/allowed/file1.txt',
    '/path/to/allowed/file2.txt',
    # Add more allowed file paths here
}

def is_file_allowed(file_path):
    """Check if the file path is in the whitelist."""
    return file_path in ALLOWED_FILES

def delete_file(file_path):
    """Securely delete a file if it's in the whitelist."""
    if not is_file_allowed(file_path):
        print("Error: File not in allowed list.")
        return False
    
    try:
        # Generate a secure random token for deletion confirmation
        token = secrets.token_hex(16)
        print(f"Deletion token: {token}")
        
        # Wait for user confirmation (implement proper confirmation mechanism)
        user_confirm = input("Type the token to confirm deletion: ")
        if user_confirm != token:
            print("Error: Deletion cancelled.")
            return False
        
        # Securely delete the file
        with open(file_path, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Overwrite the file with random data before deletion
        with open(file_path, 'wb') as f:
            f.write(secrets.token_bytes(len(file_content)))
            f.flush()
            os.fsync(f.fileno())
        
        os.remove(file_path)
        print("File deleted successfully.")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False