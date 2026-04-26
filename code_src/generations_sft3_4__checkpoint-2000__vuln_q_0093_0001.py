import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
from pathlib import Path
import os

def parse_xml_safely(file_path: str, max_size_mb: int = 10) -> ET.Element:
    """
    Safely parse XML file using defusedxml with security measures.
    
    Args:
        file_path: Path to XML file
        max_size_mb: Maximum allowed file size in MB
    
    Returns:
        Parsed XML root element
    
    Raises:
        ValueError: If file validation fails
        ET.ParseError: If XML parsing fails
    """
    # Validate file path
    try:
        file_path = Path(file_path).resolve()
        if not file_path.is_file():
            raise ValueError("Invalid file path")
    except (TypeError, ValueError):
        raise ValueError("Invalid file path")

    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValueError(f"File size exceeds {max_size_mb}MB limit")

    try:
        # Use defusedxml for safer parsing
        tree = parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        raise ET.ParseError(f"XML parsing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        root = parse_xml_safely("example.xml")
        # Process the XML safely here
    except (ValueError, ET.ParseError) as e:
        print(f"Error: {str(e)}")