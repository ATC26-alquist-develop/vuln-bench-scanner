import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import os

def safe_parse_xml(xml_file_path):
    """
    Safely parse an XML file using defusedxml to prevent XML vulnerabilities.
    
    Args:
        xml_file_path (str): Path to the XML file to be parsed
        
    Returns:
        ET.Element: Root element of the parsed XML tree
        
    Raises:
        ValueError: If the file path is invalid or file doesn't exist
        ET.ParseError: If the XML is malformed
    """
    # Validate file path
    if not xml_file_path or not isinstance(xml_file_path, str):
        raise ValueError("Invalid file path")
        
    # Check if file exists and is a file
    if not os.path.isfile(xml_file_path):
        raise ValueError(f"File not found: {xml_file_path}")
        
    try:
        # Use defusedxml for secure parsing
        tree = parse(xml_file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        raise ET.ParseError(f"Error parsing XML: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

# Example usage
try:
    xml_path = "path/to/your/file.xml"
    root = safe_parse_xml(xml_path)
    print(f"Successfully parsed XML with {len(root)} root elements")
except Exception as e:
    print(f"Error: {str(e)}")