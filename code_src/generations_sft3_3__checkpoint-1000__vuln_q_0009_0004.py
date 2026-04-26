import defusedxml.ElementTree as ET
from pathlib import Path

def read_xml_config(file_path: str) -> dict:
    """
    Securely read configuration data from an XML file.
    
    Args:
        file_path (str): Path to the XML file
        
    Returns:
        dict: Parsed configuration data
        
    Raises:
        ValueError: If file path is invalid or XML is malformed
        FileNotFoundError: If file doesn't exist
    """
    try:
        # Validate and resolve path
        path = Path(file_path).resolve()
        
        # Check if file exists
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Parse XML safely using defusedxml
        tree = ET.parse(str(path))
        root = tree.getroot()
        
        # Convert XML to dictionary
        config = {}
        for child in root:
            config[child.tag] = child.text
            
        return config
        
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading XML file: {str(e)}")