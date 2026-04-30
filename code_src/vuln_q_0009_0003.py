```python
import os
from typing import Optional
from defusedxml.ElementTree import parse
from pathlib import Path

def parse_xml_safely(file_path: str, max_file_size: int = 1024 * 1024) -> Optional[dict]:
    """
    Safely parse XML data from a file using ElementTree with security measures.
    
    Args:
        file_path: Path to the XML file
        max_file_size: Maximum allowed file size in bytes (default 1MB)
        
    Returns:
        Dictionary containing parsed XML data or None if parsing fails
    """
    try:
        # Validate and sanitize file path
        file_path = os.path.abspath(file_path)
        if not file_path.lower().endswith('.xml'):
            raise ValueError("File must have .xml extension")

        # Check file size
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exist")
            
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            raise ValueError(f"File exceeds maximum size of {max_file_size} bytes")

        # Parse XML using defusedxml (secure against XXE and other attacks)
        with open(file_path, 'rb') as file:
            tree = parse(file)
            root = tree.getroot()

        # Convert to dictionary (example implementation)
        result = {}
        for child in root:
            result[child.tag] = child.text

        return result

    except (OSError, ValueError, FileNotFoundError) as e:
        # Log error here if needed
        return None
    except Exception as e:
        # Catch any other exceptions without exposing details
        return None
```