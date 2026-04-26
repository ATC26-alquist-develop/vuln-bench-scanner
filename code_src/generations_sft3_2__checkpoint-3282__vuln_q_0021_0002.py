from defusedxml import ElementTree as ET
from typing import List, Dict
import re

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove any non-alphanumeric characters except hyphens and spaces
    return re.sub(r'[^\w\s-]', '', user_input)

def query_products_by_category(xml_file: str, category: str) -> List[Dict[str, str]]:
    """
    Safely query products by category using XPath.
    
    Args:
        xml_file: Path to the XML file
        category: Category name to search for
        
    Returns:
        List of dictionaries containing product information
        
    Raises:
        ValueError: If inputs are invalid
        ET.ParseError: If XML parsing fails
    """
    # Validate inputs
    if not xml_file or not category:
        raise ValueError("XML file path and category name are required")
    
    if not isinstance(category, str) or len(category) > 100:
        raise ValueError("Invalid category name")
    
    # Sanitize inputs
    category = sanitize_input(category)
    
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Create safe XPath expression
        xpath_expr = f".//product[contains(@category, '{category}')]/*"
        
        # Query products
        products = []
        for product in root.findall(xpath_expr):
            # Extract only safe attributes
            product_info = {
                'name': product.findtext('name', ''),
                'price': product.findtext('price', ''),
                'description': product.findtext('description', '')
            }
            products.append(product_info)
            
        return products
        
    except ET.ParseError as e:
        raise ET.ParseError(f"XML parsing error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

# Example usage
try:
    result = query_products_by_category('products.xml', 'electronics')
    print(result)
except (ValueError, ET.ParseError, Exception) as e:
    print(f"Error: {str(e)}")