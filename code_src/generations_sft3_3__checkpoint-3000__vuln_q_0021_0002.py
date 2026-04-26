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
        raise ValueError("Invalid input parameters")
    
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category must be a non-empty string")

    # Sanitize inputs
    category = sanitize_input(category)
    
    # Ensure file exists and is readable
    if not os.path.isfile(xml_file):
        raise FileNotFoundError("XML file not found")
    
    # Parse XML safely using defusedxml
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ET.ParseError(f"XML parsing error: {str(e)}")

    # Construct safe XPath query
    xpath_query = f".//product[contains(@category, '{category}')]"

    # Find matching products
    products = []
    for product in root.findall(xpath_query):
        # Extract product information (example - adjust as needed)
        product_info = {
            'id': product.get('id', ''),
            'name': product.findtext('name', ''),
            'category': product.findtext('category', '')
        }
        products.append(product_info)

    return products

# Example usage
try:
    result = query_products_by_category('products.xml', 'electronics')
    print(result)
except (ValueError, FileNotFoundError, ET.ParseError) as e:
    print(f"Error: {str(e)}")