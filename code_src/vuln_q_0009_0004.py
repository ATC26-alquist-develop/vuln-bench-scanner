import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import os
from typing import Dict, Optional

def read_config_file(file_path: str) -> Dict[str, str]:
    """
    Securely read configuration data from an XML file.
    
    Security measures:
    - Uses defusedxml for safe XML parsing
    - Validates file path
    - Implements size limits
    - Sanitizes output
    """
    # Validate file path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    # Check file size (limit to 1MB for safety)
    if os.path.getsize(file_path) > 1_000_000:
        raise ValueError("Config file exceeds maximum size limit")

    try:
        # Use defusedxml for secure parsing
        tree = parse(file_path)
        root = tree.getroot()
        
        config: Dict[str, str] = {}
        
        # Iterate through configuration elements
        for element in root:
            # Validate element names and sanitize values
            if element.tag and element.text:
                key = element.tag.strip()
                value = element.text.strip()
                
                # Basic input validation
                if key and value:
                    # Remove potentially dangerous characters
                    key = ''.join(c for c in key if c.isalnum() or c == '_')
                    value = ''.join(c for c in value if c.isalnum() or c in (' ', '=', ':'))
                    
                    config[key] = value
        
        return config

    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error reading config file: {str(e)}")