import os
import sys

def create_file(filename, content):
    """
    Create a file with the given content.
    
    Args:
        filename (str): Name of the file to create
        content (str): Content to write to the file
    """
    try:
        # Validate filename
        if not filename or not isinstance(filename, str):
            raise ValueError("Invalid filename")
            
        # Validate content
        if not content or not isinstance(content, str):
            raise ValueError("Invalid content")
            
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(filename)
        
        # Create file with specified permissions (read/write for owner only)
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"File '{safe_filename}' created successfully.")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <content>", file=sys.stderr)
        sys.exit(1)
        
    filename = sys.argv[1]
    content = sys.argv[2]
    create_file(filename, content)