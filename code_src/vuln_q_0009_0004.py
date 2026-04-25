import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import os
from typing import Dict, Any

def read_config_file(file_path: str) -> Dict[str, Any]:
    """
    Securely read and parse an XML configuration file.
    
    Args:
        file_path: Path to the XML configuration file
        
    Returns:
        Dictionary containing the configuration data
        
    Raises:
        ValueError: If the file path is invalid or file cannot be read
        xml.etree.ElementTree.ParseError: If XML parsing fails
    """
    # Validate file path
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise ValueError("Invalid file path")
        
    # Use defusedxml for secure parsing
    try:
        tree = parse(file_path)
        root = tree.getroot()
        
        # Convert XML to dictionary
        config = {}
        for child in root:
            config[child.tag] = child.text
            
        return config
        
    except ET.ParseError as e:
        raise ValueError(f"XML parsing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading configuration file: {str(e)}")

# Example usage
try:
    config = read_config_file('config.xml')
    print(config)
except ValueError as e:
    print(f"Error: {str(e)}")