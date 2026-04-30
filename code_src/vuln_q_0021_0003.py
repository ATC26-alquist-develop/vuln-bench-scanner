from defusedxml.ElementTree import fromstring, parse
from defusedxml.ElementTree import ParseError
import re

def safe_xpath_query(xml_string, xpath_expression):
    """
    Safely parse XML and perform XPath query.
    
    Args:
        xml_string (str): XML content as string
        xpath_expression (str): XPath expression to evaluate
    
    Returns:
        list: List of matching elements
    
    Raises:
        ValueError: If input validation fails
        ParseError: If XML parsing fails
    """
    # Input validation
    if not isinstance(xml_string, str) or not isinstance(xpath_expression, str):
        raise ValueError("Both inputs must be strings")
    
    if not xml_string.strip() or not xpath_expression.strip():
        raise ValueError("Inputs cannot be empty")
    
    # Validate XML string
    try:
        root = fromstring(xml_string)
    except ParseError as e:
        raise ValueError(f"Invalid XML: {e}")
    
    # Validate XPath expression
    if not re.match(r'^[\w\s\[\].\(\)]+$', xpath_expression):
        raise ValueError("Invalid XPath expression")
    
    try:
        return root.findall(xpath_expression, namespaces={'ns': 'http://example.com/ns'})
    except Exception as e:
        raise ValueError(f"XPath query failed: {e}")