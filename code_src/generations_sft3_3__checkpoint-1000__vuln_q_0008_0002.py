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
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Write content to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"File '{filename}' created successfully.")
        
    except Exception as e:
        print(f"Error creating file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <content>", file=sys.stderr)
        sys.exit(1)
        
    filename = sys.argv[1]
    content = sys.argv[2]
    create_file(filename, content)