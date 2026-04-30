import defusedxml.ElementTree as ET
from defusedxml.ElementTree import ParseError
import os
from typing import Dict, Optional

def read_config_safely(config_path: str, max_size: int = 1024 * 1024) -> Optional[Dict]:
    """
    Safely read configuration from an XML file.
    
    Args:
        config_path: Path to the XML configuration file
        max_size: Maximum allowed file size in bytes (default 1MB)
    
    Returns:
        Dictionary containing configuration data or None if error occurs
    """
    try:
        # Validate file path
        if not os.path.abspath(config_path).endswith('.xml'):
            raise ValueError("Invalid file extension. Only .xml files are allowed.")
            
        # Check file size
        if os.path.getsize(config_path) > max_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size} bytes.")
            
        # Parse XML safely
        tree = ET.parse(config_path)
        root = tree.getroot()
        
        # Convert XML to dictionary (implement your own conversion logic)
        config_data = xml_to_dict(root)
        
        return config_data
        
    except (ParseError, ValueError, OSError) as e:
        print(f"Error reading configuration: {str(e)}")
        return None

def xml_to_dict(element) -> Dict:
    """
    Convert XML element to dictionary (implement your own conversion logic).
    This is a placeholder and should be replaced with proper XML parsing.
    """
    return {element.tag: element.text if element.text else {}}