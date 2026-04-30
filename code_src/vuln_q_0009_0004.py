import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import os

def read_config(file_path):
    """
    Securely read configuration data from an XML file.
    
    Args:
        file_path (str): Path to the XML configuration file
        
    Returns:
        dict: Dictionary containing configuration data
        
    Raises:
        ValueError: If the file path is invalid or file cannot be read
        ET.ParseError: If the XML file is malformed
    """
    # Validate file path
    if not isinstance(file_path, str):
        raise ValueError("File path must be a string")
        
    if not file_path:
        raise ValueError("File path cannot be empty")
        
    # Sanitize file path to prevent directory traversal
    file_path = os.path.abspath(file_path)
    
    # Check if file exists and is a regular file
    if not os.path.isfile(file_path):
        raise ValueError("Invalid file path or file does not exist")
        
    try:
        # Use defusedxml for secure parsing
        tree = parse(file_path)
        root = tree.getroot()
        
        # Convert XML to dictionary
        config = {}
        for child in root:
            config[child.tag] = child.text
            
        return config
        
    except ET.ParseError as e:
        raise ET.ParseError(f"Invalid XML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading configuration: {str(e)}")