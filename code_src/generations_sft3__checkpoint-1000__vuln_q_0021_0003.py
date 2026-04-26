from defusedxml.ElementTree import parse
from defusedxml.ElementTree import fromstring
import re

def get_employee_info(xml_string):
    """
    Search an XML document for employee information using a secure XPath query.
    
    Args:
        xml_string (str): XML document as a string
        
    Returns:
        list: List of dictionaries containing employee information
        
    Raises:
        ValueError: If input is not a valid XML string
    """
    # Input validation
    if not isinstance(xml_string, str):
        raise ValueError("Input must be a string")
        
    # Check if XML is well-formed
    try:
        root = fromstring(xml_string)
    except Exception as e:
        raise ValueError(f"Invalid XML: {str(e)}")
        
    # Define XPath query
    xpath_query = "//employee"
    
    # Get employee information using XPath
    employees = root.findall(xpath_query)
    
    # Process results
    result = []
    for employee in employees:
        # Extract employee information
        name = employee.findtext("name", "")
        department = employee.findtext("department", "")
        salary = employee.findtext("salary", "")
        
        # Validate extracted data
        if not all([name, department, salary]):
            continue
            
        # Sanitize input
        name = re.sub(r'[^\w\s]', '', name)
        department = re.sub(r'[^\w\s]', '', department)
        salary = re.sub(r'[^\d.]', '', salary)
        
        result.append({
            "name": name,
            "department": department,
            "salary": float(salary)
        })
        
    return result