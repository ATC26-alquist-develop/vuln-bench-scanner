from defusedxml import ElementTree
import os
from typing import Optional

def parse_xml_safely(file_path: str, max_size: int = 1024 * 1024) -> Optional[ElementTree.Element]:
    """
    Safely parse XML file using defusedxml library.
    
    Args:
        file_path: Path to XML file
        max_size: Maximum allowed file size in bytes (default 1MB)
    
    Returns:
        ElementTree.Element or None if parsing fails
    """
    try:
        # Validate file path
        if not os.path.exists(file_path):
            raise ValueError("File does not exist")
            
        # Check file size
        if os.path.getsize(file_path) > max_size:
            raise ValueError(f"File size exceeds {max_size} bytes limit")
            
        # Parse XML safely
        tree = ElementTree.parse(file_path)
        root = tree.getroot()
        
        return root
        
    except (ElementTree.ParseError, ValueError, OSError) as e:
        # Log error here if needed
        return None
    except Exception:
        # Catch all other exceptions without exposing details
        return None