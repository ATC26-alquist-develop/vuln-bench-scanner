import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import io

def safe_parse_xml(xml_string):
    """
    Safely parse XML string using defusedxml to prevent XXE attacks
    and other XML vulnerabilities.
    
    Args:
        xml_string (str): The XML content to parse
        
    Returns:
        ElementTree.Element: The root element of the parsed XML
        
    Raises:
        ValueError: If the XML is invalid
        ET.ParseError: If parsing fails
    """
    try:
        # Use defusedxml for secure parsing
        tree = parse(io.StringIO(xml_string))
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {str(e)}")

# Example usage:
# xml_content = "<root><element>data</element></root>"
# root = safe_parse_xml(xml_content)