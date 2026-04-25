from defusedxml import ElementTree
import os
from typing import Optional

def parse_xml_safely(file_path: str, max_size_mb: int = 10) -> Optional[ElementTree.Element]:
    """
    Safely parse XML file using defusedxml library.
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB (default 10MB)
    
    Returns:
        ElementTree.Element or None if parsing fails
    """
    # Validate file path
    if not os.path.exists(file_path):
        return None
        
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return None
        
    try:
        # Parse XML safely using defusedxml
        tree = ElementTree.parse(file_path)
        root = tree.getroot()
        return root
    except (ElementTree.ParseError, OSError):
        return None