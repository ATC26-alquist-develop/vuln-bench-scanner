from typing import List, Dict
import re

def get_employee_info(xml_file: str, employee_id: str) -> List[Dict[str, str]]:
    """
    Search for employee information using XPath query based on employee ID.
    
    Args:
        xml_file: Path to XML file containing employee data
        employee_id: Employee ID to search for
        
    Returns:
        List of dictionaries containing employee information
        
    Raises:
        ValueError: If employee_id is invalid
        FileNotFoundError: If XML file doesn't exist
        Exception: For other XML parsing errors
    """
    # Input validation
    if not isinstance(xml_file, str) or not isinstance(employee_id, str):
        raise ValueError("Invalid input types")
        
    # Validate employee_id format (alphanumeric and hyphens only)
    if not re.match(r'^[a-zA-Z0-9-]+$', employee_id):
        raise ValueError("Invalid employee ID format")
        
    # Read XML file
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {xml_file}")
        
    # Construct XPath query
    xpath_query = f"//employee[@id='{employee_id}']"
    
    # Parse XML and extract employee info
    from defusedxml import ElementTree as ET
    try:
        root = ET.fromstring(xml_content)
        employee = root.find(xpath_query)
        
        if employee is None:
            return []
            
        return {
            'name': employee.findtext('name', ''),
            'department': employee.findtext('department', ''),
            'position': employee.findtext('position', '')
        }
        
    except ET.ParseError as e:
        raise Exception(f"XML parsing error: {str(e)}")