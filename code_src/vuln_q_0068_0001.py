from defusedxml import ElementTree
from io import StringIO
import sys

def parse_xml_safely(xml_string: str) -> ElementTree.Element:
    """
    Safely parse XML data using defusedxml library.
    
    Args:
        xml_string: String containing XML data
        
    Returns:
        ElementTree.Element: Root element of parsed XML
        
    Raises:
        ValueError: If XML is invalid or contains security vulnerabilities
        TypeError: If input is not a string
    """
    if not isinstance(xml_string, str):
        raise TypeError("Input must be a string")
        
    if not xml_string:
        raise ValueError("Empty XML string provided")
        
    try:
        # Use StringIO to handle string input safely
        xml_file = StringIO(xml_string)
        
        # Parse XML using defusedxml
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        
        return root
        
    except ElementTree.ParseError as e:
        raise ValueError(f"Invalid XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {str(e)}")