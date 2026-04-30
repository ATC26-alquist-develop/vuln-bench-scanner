```python
from defusedxml import ElementTree as SafeET
import os
from typing import Dict, Optional
import logging

def parse_xml_safely(file_path: str, max_file_size: int = 1024 * 1024) -> Optional[Dict]:
    """
    Safely parse XML file and extract information.
    
    Args:
        file_path: Path to the XML file
        max_file_size: Maximum allowed file size in bytes (default 1MB)
        
    Returns:
        Dictionary containing extracted information or None if parsing fails
    """
    # Validate input
    if not file_path or not isinstance(file_path, str):
        logging.error("Invalid file path")
        return None
        
    # Validate file exists and check size
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return None
        
    try:
        # Check file size
        if os.path.getsize(file_path) > max_file_size:
            logging.error(f"File exceeds maximum size of {max_file_size} bytes")
            return None
            
        # Initialize result dictionary
        result: Dict = {}
        
        try:
            # Parse XML using defusedxml (safe against XXE attacks)
            tree = SafeET.parse(file_path)
            root = tree.getroot()
            
            # Example: Extract all 'item' elements
            for item in root.findall('.//item'):
                # Extract and sanitize text content
                name = item.find('name')
                if name is not None:
                    result[name.text.strip()] = name.text.strip()
                    
            return result
            
        except SafeET.ParseError as e:
            logging.error(f"XML parsing error: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        
    return None

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Example file path (replace with actual path)
    file_path = "example.xml"
    
    # Parse XML
    data = parse_xml_safely(file_path)
    
    if data:
        logging.info(f"Successfully parsed XML. Extracted data: {data}")
    else:
        logging.error("Failed to parse XML")
```