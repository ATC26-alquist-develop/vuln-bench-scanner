from defusedxml.ElementTree import parse
import os
from typing import Optional

def parse_xml_safely(file_path: str, max_size_mb: int = 10) -> Optional[dict]:
    """
    Safely parse XML file using defusedxml library.
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Parsed XML data as dictionary or None if parsing fails
    """
    # Validate file path
    if not isinstance(file_path, str):
        return None
        
    # Check file extension
    if not file_path.lower().endswith('.xml'):
        return None
        
    # Validate file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return None
        
    try:
        # Parse XML safely using defusedxml
        tree = parse(file_path)
        root = tree.getroot()
        
        # Convert to dictionary (customize as needed)
        def xml_to_dict(element):
            result = {}
            for child in element:
                if len(child) == 0:
                    result[child.tag] = child.text
                else:
                    result[child.tag] = xml_to_dict(child)
            return result
            
        return xml_to_dict(root)
        
    except Exception:
        # Return None on any parsing error
        return None