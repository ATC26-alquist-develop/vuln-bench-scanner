from defusedxml import ElementTree as ET
from pathlib import Path
import os
from typing import Dict, Optional

def parse_xml_safely(file_path: str, max_size_mb: int = 10) -> Optional[Dict]:
    """
    Safely parse XML file and extract information.
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Dictionary containing extracted information or None if error occurs
    """
    try:
        # Validate file path
        path = Path(file_path).resolve()
        if not path.is_file():
            raise ValueError("Invalid file path")
            
        # Check file size
        if path.stat().st_size > max_size_mb * 1024 * 1024:
            raise ValueError(f"File too large (max {max_size_mb}MB)")
            
        # Parse XML safely using defusedxml
        tree = ET.parse(str(path))
        root = tree.getroot()
        
        # Extract information (example: all element names)
        data = {elem.tag: elem.text for elem in root.iter() if elem.text}
        
        return data
        
    except (ET.ParseError, ValueError, OSError) as e:
        # Log error here if needed
        return None
    except Exception:
        # Catch all other exceptions without exposing details
        return None

# Example usage
if __name__ == "__main__":
    result = parse_xml_safely("example.xml")
    if result:
        print("Parsed data:", result)
    else:
        print("Failed to parse XML")