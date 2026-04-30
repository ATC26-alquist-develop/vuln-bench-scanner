from defusedxml import ElementTree as ET
from io import StringIO

def safe_parse_xml(xml_string: str) -> ElementTree.Element:
    """
    Safely parse XML data using defusedxml library.
    
    Args:
        xml_string: String containing XML data
        
    Returns:
        ElementTree.Element: Root element of the parsed XML
        
    Raises:
        ValueError: If XML is invalid or parsing fails
    """
    try:
        # Use StringIO to handle string input safely
        xml_file = StringIO(xml_string)
        # Parse XML safely using defusedxml
        root = ET.fromstring(xml_file.read())
        return root
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {str(e)}")