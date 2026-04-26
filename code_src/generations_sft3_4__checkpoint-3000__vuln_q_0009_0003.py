from defusedxml import ElementTree as ET
import os
from typing import Optional

def parse_xml_safely(file_path: str, max_size: int = 1024 * 1024) -> Optional[ET.Element]:
    """
    Safely parse XML file using defusedxml library with security controls.
    
    Args:
        file_path: Path to XML file
        max_size: Maximum allowed file size in bytes (default 1MB)
    
    Returns:
        Parsed XML root element or None if error occurs
    """
    try:
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exist")
            
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size} bytes")
            
        # Parse XML safely using defusedxml
        tree = ET.parse(file_path)
        return tree.getroot()
        
    except (ET.ParseError, ValueError, FileNotFoundError) as e:
        # Log error here if needed
        print(f"Error parsing XML: {str(e)}")
        return None
    except Exception as e:
        # Catch all other exceptions without exposing details
        print("Unexpected error occurred")
        return None

# Example usage
if __name__ == "__main__":
    xml_path = "example.xml"
    root = parse_xml_safely(xml_path)
    if root is not None:
        # Process the XML safely here
        pass