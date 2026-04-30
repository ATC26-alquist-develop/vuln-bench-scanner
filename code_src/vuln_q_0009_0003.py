```python
from defusedxml.ElementTree import fromstring
import os

def safe_parse_xml(file_path, max_size_mb=10):
    """
    Safely parse XML file using defusedxml library.
    
    Args:
        file_path (str): Path to XML file
        max_size_mb (int): Maximum allowed file size in MB
    
    Returns:
        ElementTree.Element: Parsed XML root element
    
    Raises:
        ValueError: If file path is invalid or file is too large
        OSError: If file cannot be read
    """
    # Validate file path
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("Invalid file path")
    
    # Normalize path and check if file exists
    file_path = os.path.abspath(file_path)
    if not os.path.isfile(file_path):
        raise ValueError("File does not exist")
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValueError(f"File size exceeds maximum allowed size of {max_size_mb}MB")
    
    try:
        # Safely parse XML using defusedxml
        root = fromstring(file_path)
        return root
    except Exception as e:
        raise OSError(f"Error parsing XML: {str(e)}")
```