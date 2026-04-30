from defusedxml import ElementTree as ET
from typing import Optional

def search_employee_info(xml_file: str, xpath_query: str) -> Optional[dict]:
    """
    Search an XML file for employee information using a given XPath query.
    
    Args:
        xml_file: Path to the XML file
        xpath_query: XPath query to search for employee information
        
    Returns:
        Dictionary containing employee information if found, None otherwise
        
    Raises:
        ValueError: If the XML file is not well-formed
        FileNotFoundError: If the XML file does not exist
        ET.ParseError: If the XML file is not well-formed
    """
    try:
        # Parse the XML file safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find the first matching element
        result = root.find(xpath_query)
        
        if result is None:
            return None
            
        # Convert the result to a dictionary
        employee_info = {}
        for child in result:
            employee_info[child.tag] = child.text
            
        return employee_info
        
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {xml_file}")
    except Exception as e:
        raise ValueError(f"Error processing XML file: {e}")