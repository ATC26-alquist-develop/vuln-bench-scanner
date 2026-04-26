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
        ValueError: If category input is invalid
        FileNotFoundError: If XML file doesn't exist
        ET.ParseError: If XML file is malformed
    """
    # Validate category input
    if not category or not isinstance(category, str):
        raise ValueError("Invalid category input")
    
    category = sanitize_input(category)
    
    # Validate file path
    if not xml_file or not isinstance(xml_file, str):
        raise ValueError("Invalid XML file path")
    
    # Ensure file exists
    if not os.path.exists(xml_file):
        raise FileNotFoundError(f"XML file not found: {xml_file}")
    
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Safely construct XPath query
        xpath_query = f"//product[category/text() = '{category}']"
        
        # Query products
        products = root.findall(xpath_query)
        
        # Process results
        result = []
        for product in products:
            product_info = {
                'name': product.findtext('name', ''),
                'description': product.findtext('description', ''),
                'price': product.findtext('price', '')
            }
            result.append(product_info)
            
        return result
        
    except ET.ParseError as e:
        raise ET.ParseError(f"XML parsing error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing XML: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        products = query_products_by_category("products.xml", "electronics")
        for product in products:
            print(product)
    except Exception as e:
        print(f"Error: {str(e)}")