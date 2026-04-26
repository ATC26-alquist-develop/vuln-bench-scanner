from defusedxml import ElementTree as ET
import os
from pathlib import Path
import logging

def parse_xml_safely(file_path: str, max_size_mb: int = 10) -> ET.Element:
    """
    Safely parse XML file using defusedxml library
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Parsed XML root element
        
    Raises:
        ValueError: If file validation fails
        OSError: If file operations fail
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Validate file path
        file_path = os.path.abspath(file_path)
        path = Path(file_path)
        
        # Validate file exists and is a file
        if not path.is_file():
            raise ValueError("Invalid file path")
            
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size_mb}MB")
            
        # Parse XML safely using defusedxml
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Log successful parsing
        logger.info(f"Successfully parsed XML file: {file_path}")
        return root
        
    except ET.ParseError as e:
        logger.error(f"XML parsing error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing XML file: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        root = parse_xml_safely("example.xml")
        # Process the XML data safely here
    except Exception as e:
        logging.error(f"Failed to parse XML: {str(e)}")