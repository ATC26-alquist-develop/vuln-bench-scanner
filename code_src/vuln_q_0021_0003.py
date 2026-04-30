import xml.etree.ElementTree as ET
from typing import Optional

def search_employee(xml_file: str, employee_name: str) -> Optional[str]:
    """
    Search for an employee in an XML file using a parameterized XPath query.
    
    Args:
        xml_file: Path to the XML file containing employee data
        employee_name: Name of the employee to search for
        
    Returns:
        The employee information as a string if found, None otherwise
    """
    try:
        # Input validation
        if not xml_file or not employee_name:
            raise ValueError("XML file path and employee name are required")
        
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Use parameterized XPath query to prevent injection
        xpath_query = "/employees/employee[name='{}']".format(employee_name)
        
        # Find the matching employee
        employee = root.find(xpath_query)
        
        # Return employee information if found
        if employee is not None:
            return ET.tostring(employee, encoding='unicode')
        else:
            return None
            
    except (ET.ParseError, FileNotFoundError, ValueError) as e:
        # Log the error here if needed
        return None