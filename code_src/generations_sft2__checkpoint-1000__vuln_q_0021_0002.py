from defusedxml import ElementTree
from typing import List, Dict
import re

def search_products_by_category(xml_file: str, category: str) -> List[Dict[str, str]]:
    """
    Securely search products by category using XPath
    
    Args:
        xml_file: Path to the XML file
        category: Category to search for
        
    Returns:
        List of dictionaries containing product details
    """
    # Validate input
    if not isinstance(xml_file, str) or not isinstance(category, str):
        raise ValueError("Invalid input types")
        
    if not xml_file or not category:
        raise ValueError("Empty input")
        
    # Sanitize category input
    category = re.sub(r'[^\w\s-]', '', category)
    
    try:
        # Parse XML safely using defusedxml
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        
        # Define safe XPath query
        xpath_query = f".//product[@category='{category}']"
        
        # Find matching products
        products = root.findall(xpath_query)
        
        # Extract product details
        result = []
        for product in products:
            product_dict = {
                'name': product.find('name').text if product.find('name') is not None else '',
                'price': product.find('price').text if product.find('price') is not None else '',
                'description': product.find('description').text if product.find('description') is not None else ''
            }
            result.append(product_dict)
            
        return result
        
    except ElementTree.ParseError as e:
        raise ValueError(f"Invalid XML file: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing XML: {str(e)}")