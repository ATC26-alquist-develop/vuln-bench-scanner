from typing import List, Dict
from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

def get_employee_info(xml_file: str) -> List[Dict[str, str]]:
    """
    Search XML file for employee information using XPath query.
    
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
        
        # Define XPath query
        xpath_query = ".//employee"
        
        # Find all employee elements
        employees = root.findall(xpath_query)
        
        # Process each employee element
        employee_info = []
        for emp in employees:
            # Extract employee data using XPath attributes
            emp_info = {
                "name": emp.findtext("name", ""),
                "department": emp.findtext("department", ""),
                "position": emp.findtext("position", "")
            }
            employee_info.append(emp_info)
            
        return employee_info
        
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {e}")
    except Exception as e:
        raise ValueError(f"Error processing XML file: {e}")