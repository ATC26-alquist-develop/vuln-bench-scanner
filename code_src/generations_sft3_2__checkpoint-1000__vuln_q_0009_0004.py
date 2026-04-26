import xml.etree.ElementTree as ET
from typing import Dict, Any
import os

def read_xml_config(file_path: str) -> Dict[str, Any]:
    """
    Securely read configuration data from an XML file.
    
    Args:
        file_path (str): Path to the XML file
        
    Returns:
        Dict[str, Any]: Dictionary containing configuration data
        
    Raises:
        ValueError: If file path is invalid or XML is malformed
        FileNotFoundError: If file doesn't exist
    """
    # Validate file path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"XML file not found: {file_path}")
        
    # Validate file extension
    if not file_path.lower().endswith('.xml'):
        raise ValueError("File must have .xml extension")
        
    try:
        # Parse XML using ElementTree
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Convert XML to dictionary
        config = {}
        for child in root:
            config[child.tag] = child.text
            
        return config
        
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading XML file: {str(e)}")