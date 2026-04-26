from defusedxml.ElementTree import parse
from defusedxml.ElementTree import fromstring
import re

def get_employee_info(xml_string):
    """
    Search an XML document for employee information using a constructed XPath query.
    
    Args:
        xml_string (str): XML document as a string
        
    Returns:
        list: List of dictionaries containing employee information
        
    Raises:
        ValueError: If the XML is invalid or contains no employees
    """
    # Validate input
    if not isinstance(xml_string, str):
        raise ValueError("Input must be a string")
        
    # Parse XML safely using defusedxml
    try:
        root = fromstring(xml_string)
    except Exception as e:
        raise ValueError(f"Invalid XML: {str(e)}")

    # Construct XPath query
    xpath_query = ".//employee"
    
    # Find all employees
    employees = root.findall(xpath_query)
    
    # Validate result
    if not employees:
        raise ValueError("No employees found in XML")
        
    # Process employee data
    result = []
    for employee in employees:
        # Extract employee information
        name = employee.findtext("name", "")
        position = employee.findtext("position", "")
        salary = employee.findtext("salary", "")
        
        # Validate extracted data
        if not all([name, position, salary]):
            raise ValueError("Invalid employee data")
            
        # Create dictionary with sanitized data
        employee_data = {
            "name": name.strip(),
            "position": position.strip(),
            "salary": salary.strip()
        }
        
        result.append(employee_data)
        
    return result