from defusedxml import ElementTree as ET
from typing import List, Dict
import re
from urllib.parse import urlparse
import html

class SecureXMLQuery:
    def __init__(self, xml_file_path: str):
        # Validate and sanitize file path
        if not self._is_safe_path(xml_file_path):
            raise ValueError("Invalid or unsafe XML file path")
        
        self.xml_file_path = xml_file_path
        self.tree = None
        self.root = None

    def _is_safe_path(self, path: str) -> bool:
        """Validate file path for security"""
        try:
            parsed = urlparse(path)
            return all([parsed.scheme == '', parsed.netloc == ''])
        except Exception:
            return False

    def load_xml(self) -> None:
        """Securely load XML file"""
        try:
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
        except Exception as e:
            raise ValueError(f"Failed to load XML file: {str(e)}")

    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input"""
        return html.escape(input_string)

    def validate_category(self, category: str) -> bool:
        """Validate category input"""
        return bool(re.match(r'^[a-zA-Z0-9\s]+$', category))

    def query_products_by_category(self, category: str) -> List[Dict[str, str]]:
        """Securely query products by category"""
        if not self.root:
            raise ValueError("XML file not loaded")

        if not self.validate_category(category):
            raise ValueError("Invalid category format")

        sanitized_category = self.sanitize_input(category)
        
        # Use defusedxml for secure XPath query
        xpath_query = f"//product[contains(@category, '{sanitized_category}')]"

        try:
            results = self.root.findall(xpath_query)
            return [self._extract_product_info(product) for product in results]
        except Exception as e:
            raise ValueError(f"XPath query failed: {str(e)}")

    def _extract_product_info(self, product: ET.Element) -> Dict[str, str]:
        """Extract product information safely"""
        return {
            'id': product.get('id', ''),
            'name': product.findtext('name', ''),
            'price': product.findtext('price', '')
        }

# Example usage
if __name__ == "__main__":
    try:
        query = SecureXMLQuery("products.xml")
        query.load_xml()
        
        category = input("Enter product category: ")
        results = query.query_products_by_category(category)
        
        for product in results:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}")
    
    except ValueError as e:
        print(f"Error: {str(e)}")