from typing import List, Dict, Any
from defusedxml import ElementTree as ET
import re

def get_employee_info(xml_file: str, employee_id: str) -> List[Dict[str, Any]]:
    """
    Search for employee information using the provided employee ID.
    
    Args:
        xml_file: Path to the XML file containing employee data
        employee_id: ID of the employee to search for
        
    Returns:
        List of dictionaries containing employee information
        
    Raises:
        ValueError: If employee_id is invalid or XML file is invalid
        FileNotFoundError: If XML file doesn't exist
    """
    # Validate employee_id
    if not re.match(r'^\d+$', employee_id):
        raise ValueError("Invalid employee ID format")
    
    # Validate XML file
    if not xml_file.endswith('.xml'):
        raise ValueError("File must be an XML file")
    
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Construct XPath query
        xpath_query = f"//employee[@id='{employee_id}']"
        
        # Find matching employee
        employee = root.find(xpath_query)
        
        if employee is None:
            return []
            
        # Extract employee information
        info = {
            'name': employee.findtext('name', ''),
            'department': employee.findtext('department', ''),
            'position': employee.findtext('position', ''),
            'salary': employee.findtext('salary', '')
        }
        
        return [info]
        
    except ET.ParseError:
        raise ValueError("Invalid XML file")
    except Exception as e:
        raise ValueError(f"Error processing XML: {str(e)}")