from defusedxml.ElementTree import fromstring, ParseError
import io

def safe_parse_xml(xml_string):
    """
    Safely parse XML string using defusedxml.
    Returns ElementTree object if successful, None otherwise.
    """
    try:
        # Use StringIO to handle string input safely
        tree = fromstring(xml_string)
        return tree
    except ParseError:
        print("Invalid XML provided")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
xml_data = """<root><element>data</element></root>"""
parsed_tree = safe_parse_xml(xml_data)
if parsed_tree is not None:
    print("XML parsed successfully")