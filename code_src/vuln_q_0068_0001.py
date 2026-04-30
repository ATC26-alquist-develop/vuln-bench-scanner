```python
import defusedxml.ElementTree as ET
from typing import Dict, Optional
import logging

def parse_xml_safely(xml_string: str, max_size: int = 1024 * 1024) -> Optional[Dict]:
    """
    Safely parse XML data using defusedxml.
    
    Args:
        xml_string: The XML data to parse
        max_size: Maximum allowed size of XML in bytes (default 1MB)
        
    Returns:
        Dictionary containing parsed XML data or None if parsing fails
    """
    try:
        # Validate input
        if not isinstance(xml_string, str):
            raise ValueError("Input must be a string")
            
        # Check size limit
        if len(xml_string.encode('utf-8')) > max_size:
            raise ValueError(f"XML data exceeds maximum size of {max_size} bytes")

        # Parse XML safely using defusedxml
        root = ET.fromstring(xml_string)
        
        # Convert to dictionary
        result = {}
        for child in root:
            result[child.tag] = child.text
            
        return result

    except ET.ParseError as e:
        logging.error(f"XML parsing error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error parsing XML: {str(e)}")
        return None
```