from defusedxml.ElementTree import parse
import os
from pathlib import Path
import logging

def parse_xml_safely(xml_file_path: str, max_size_mb: int = 10) -> dict:
    """
    Safely parse XML file using defusedxml library.
    
    Args:
        xml_file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Dictionary containing parsed XML data
        
    Raises:
        ValueError: If file validation fails
        Exception: For other parsing errors
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Convert to Path object for secure path handling
        file_path = Path(xml_file_path).resolve()
        
        # Validate file path
        if not file_path.is_file():
            raise ValueError("Invalid file path")
            
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(f"File size exceeds maximum allowed size of {max_size_mb}MB")
            
        # Parse XML safely using defusedxml
        tree = parse(file_path)
        
        # Get root element
        root = tree.getroot()
        
        # Convert to dictionary (adjust this based on your XML structure)
        def xml_to_dict(element):
            result = {}
            for child in element:
                if len(child) == 0:
                    result[child.tag] = child.text
                else:
                    result[child.tag] = xml_to_dict(child)
            return result
            
        return xml_to_dict(root)
        
    except Exception as e:
        logger.error(f"Error parsing XML: {str(e)}")
        raise