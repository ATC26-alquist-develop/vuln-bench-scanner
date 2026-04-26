from defusedxml import ElementTree as ET
from pathlib import Path
import os
from typing import Dict, Optional

def parse_xml_safely(file_path: str, max_size_mb: int = 10) -> Optional[Dict]:
    """
    Safely parse XML file with security measures.
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Dictionary with extracted information or None if error occurs
    """
    try:
        # Convert to Path object for secure path handling
        path = Path(file_path).resolve()
        
        # Security checks
        if not path.is_file():
            raise ValueError("Invalid file path")
            
        # Check file size
        if path.stat().st_size > max_size_mb * 1024 * 1024:
            raise ValueError(f"File too large (max {max_size_mb}MB)")
            
        # Parse XML safely using defusedxml
        tree = ET.parse(str(path))
        root = tree.getroot()
        
        # Extract information (example: all text elements)
        result = {}
        for elem in root.iter():
            if elem.text and elem.text.strip():
                result[elem.tag] = elem.text.strip()
                
        return result
        
    except (ET.ParseError, ValueError, OSError) as e:
        # Log error here if needed
        return None
    except Exception:
        # Catch all other exceptions without exposing details
        return None