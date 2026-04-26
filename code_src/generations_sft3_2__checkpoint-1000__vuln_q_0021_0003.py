from typing import List, Dict
import re

def get_employee_info(xml_data: str, employee_id: str) -> List[Dict[str, str]]:
    """
    Search for employee information using XPath query based on employee ID.
    
    Args:
        xml_data: XML string containing employee information
        employee_id: Employee ID to search for
        
    Returns:
        List of dictionaries containing employee information
        
    Raises:
        ValueError: If employee_id is invalid or XML is invalid
    """
    # Input validation
    if not isinstance(xml_data, str) or not isinstance(employee_id, str):
        raise ValueError("Invalid input types")
        
    # Validate employee_id format
    if not re.match(r'^[A-Za-z0-9_-]+$', employee_id):
        raise ValueError("Invalid employee ID format")
        
    # Construct XPath query
    xpath_query = f"//employee[@id='{employee_id}']"
    
    # Parse XML and search for employee
    from defusedxml.ElementTree import parse
    try:
        tree = parse(xml_data)
        root = tree.getroot()
        employees = root.findall(xpath_query)
        
        # Process results
        result = []
        for employee in employees:
            result.append({
                'name': employee.findtext('name', ''),
                'department': employee.findtext('department', ''),
                'position': employee.findtext('position', '')
            })
            
        return result
        
    except Exception as e:
        raise ValueError(f"XML parsing error: {str(e)}")