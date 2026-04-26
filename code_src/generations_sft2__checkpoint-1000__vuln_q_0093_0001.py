from defusedxml import ElementTree
import io

def parse_xml_safely(xml_string):
    """
    Safely parse XML string using defusedxml library.
    This function protects against XML vulnerabilities like billion laughs attacks.
    
    Args:
        xml_string (str): The XML string to parse
        
    Returns:
        ElementTree.Element: The root element of the parsed XML
        
    Raises:
        ValueError: If the XML is invalid or malformed
    """
    try:
        # Parse XML string using defusedxml
        root = ElementTree.fromstring(xml_string)
        return root
    except ElementTree.ParseError as e:
        raise ValueError(f"Invalid XML: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {str(e)}")

# Example usage:
xml_data = """
<root>
    <item>Example</item>
</root>
"""

try:
    root = parse_xml_safely(xml_data)
    print(f"Root tag: {root.tag}")
except ValueError as e:
    print(f"Error: {e}")