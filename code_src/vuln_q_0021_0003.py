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
    """
    try:
        # Parse XML file safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find all matching elements
        results = root.findall(xpath_query)
        
        # Process results
        if results:
            return [elem.attrib for elem in results]
        else:
            return None
            
    except ET.ParseError:
        return None
    except Exception:
        return None