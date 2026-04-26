from defusedxml.ElementTree import parse
import os
from pathlib import Path
import logging

def parse_xml_safely(xml_file_path: str, max_size_mb: int = 10) -> dict:
    """
    Safely parse XML file using defusedxml library
    
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
        
        # Convert to dictionary
        root = tree.getroot()
        return xml_to_dict(root)
        
    except Exception as e:
        logger.error(f"Error parsing XML: {str(e)}")
        raise

def xml_to_dict(element, root_name=None):
    """
    Convert XML element to dictionary recursively
    
    Args:
        element: XML element
        root_name: Optional name for root element
        
    Returns:
        Dictionary representation of XML
    """
    result = {}
    
    # Handle root element
    if root_name:
        result[root_name] = {}
    
    # Process attributes
    if element.attrib:
        result.update(element.attrib)
    
    # Process child elements
    for child in element:
        child_name = child.tag
        child_data = xml_to_dict(child)
        
        # Handle nested elements
        if isinstance(child_data, dict):
            if root_name:
                result[root_name][child_name] = child_data
            else:
                result[child_name] = child_data
        else:
            if root_name:
                result[root_name][child_name] = child_data
            else:
                result[child_name] = child_data
                
    return result