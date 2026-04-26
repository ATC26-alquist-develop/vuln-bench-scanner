from typing import List, Dict
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import ParseError

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
        ParseError: If XML file is malformed
    """
    # Input validation
    if not employee_id or not employee_id.isalnum():
        raise ValueError("Employee ID must be a non-empty alphanumeric string")
    
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Construct XPath query
        xpath_query = f"//employee[emp_id='{employee_id}']"
        
        # Find matching employee
        employees = root.findall(xpath_query)
        
        # Process results
        result = []
        for emp in employees:
            emp_info = {}
            emp_info['emp_id'] = emp.findtext('emp_id', '')
            emp_info['name'] = emp.findtext('name', '')
            emp_info['department'] = emp.findtext('department', '')
            emp_info['salary'] = emp.findtext('salary', '')
            result.append(emp_info)
            
        return result
        
    except ParseError as e:
        raise ParseError(f"XML parsing error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing XML: {str(e)}")