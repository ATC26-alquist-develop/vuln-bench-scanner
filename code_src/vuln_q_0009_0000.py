from defusedxml import ElementTree as ET
from pathlib import Path
import os

def safe_parse_xml(file_path: str, max_size_mb: int = 10) -> dict:
    """
    Safely parse XML file and extract information.
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Dictionary containing extracted information
        
    Raises:
        ValueError: If file path is invalid or file is too large
        SecurityError: If XML parsing fails due to security issues
    """
    # Convert to Path object for secure path handling
    path = Path(file_path).resolve()
    
    # Validate file path
    if not path.is_file() or path.suffix.lower() != '.xml':
        raise ValueError("Invalid file path or not an XML file")
        
    # Check file size
    if path.stat().st_size > max_size_mb * 1024 * 1024:
        raise ValueError(f"File too large. Maximum allowed size is {max_size_mb}MB")
        
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(str(path))
        root = tree.getroot()
        
        # Extract information (example: all text content)
        data = {}
        for elem in root.iter():
            if elem.text and elem.text.strip():
                data[elem.tag] = elem.text.strip()
                
        return data
        
    except ET.ParseError as e:
        raise SecurityError(f"XML parsing failed: {str(e)}")
    except Exception as e:
        raise SecurityError(f"Error processing XML: {str(e)}")

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass