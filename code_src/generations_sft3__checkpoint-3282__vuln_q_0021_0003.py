from typing import List, Dict
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

def get_employee_info(xml_file: str) -> List[Dict[str, str]]:
    """
    Search XML file for employee information using XPath.
    
    Args:
        xml_file: Path to XML file containing employee data
        
    Returns:
        List of dictionaries containing employee information
        
    Raises:
        ValueError: If XML file is invalid or empty
        FileNotFoundError: If XML file doesn't exist
    """
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Create XPath query
        xpath_query = root.find(".//employee")
        
        # Process results
        employees = []
        for employee in xpath_query:
            employee_info = {
                "name": employee.findtext("name", ""),
                "department": employee.findtext("department", ""),
                "position": employee.findtext("position", "")
            }
            employees.append(employee_info)
            
        return employees
        
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {e}")
    except Exception as e:
        raise ValueError(f"Error processing XML: {e}")