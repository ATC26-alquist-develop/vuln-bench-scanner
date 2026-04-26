from typing import List, Dict
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

def get_employee_info(xml_file: str, employee_id: str) -> List[Dict[str, str]]:
    """
    Search XML file for employee information using provided employee ID.
    
    Args:
        xml_file (str): Path to XML file
        employee_id (str): Employee ID to search for
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing employee information
        
    Raises:
        ValueError: If employee_id is empty or contains invalid characters
        FileNotFoundError: If XML file doesn't exist
        ET.ParseError: If XML file is invalid
    """
    # Input validation
    if not employee_id or not employee_id.isalnum():
        raise ValueError("Employee ID must be non-empty alphanumeric string")
    
    # Parse XML safely using defusedxml
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {xml_file}")
    except ET.ParseError as e:
        raise ET.ParseError(f"Invalid XML file: {str(e)}")

    # Find employee using XPath
    xpath_query = f"//employee[employee_id='{employee_id}']"
    try:
        employee = root.find(xpath_query)
    except AttributeError:
        return []  # Employee not found
        
    # Extract employee information
    result = []
    if employee is not None:
        result = [
            {
                'name': employee.findtext('name', ''),
                'department': employee.findtext('department', ''),
                'position': employee.findtext('position', '')
            }
        ]
    
    return result