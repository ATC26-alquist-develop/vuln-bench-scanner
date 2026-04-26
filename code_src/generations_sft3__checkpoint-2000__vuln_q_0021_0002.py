from defusedxml import ElementTree as ET
from typing import List, Dict
import re

class SecureXMLQuery:
    def __init__(self, xml_file_path: str):
        # Validate file path
        if not self._is_safe_path(xml_file_path):
            raise ValueError("Invalid or unsafe XML file path")
        
        self.xml_file_path = xml_file_path
        self.tree = None

    def _is_safe_path(self, path: str) -> bool:
        """Validate file path to prevent directory traversal"""
        return bool(re.match(r'^[a-zA-Z0-9_\-./]+\.xml$', path))

    def load_xml(self) -> None:
        """Securely load XML file using defusedxml"""
        try:
            self.tree = ET.parse(self.xml_file_path)
        except ET.ParseError:
            raise ValueError("Invalid XML file")

    def query_products_by_category(self, category: str) -> List[Dict[str, str]]:
        """Securely query products by category using XPath"""
        if not self.tree:
            raise ValueError("XML file not loaded")

        # Validate category input
        if not self._is_safe_category(category):
            raise ValueError("Invalid category input")

        # Use defusedxml for secure parsing
        root = self.tree.getroot()
        
        # Use safe XPath expression
        xpath_expression = f"//product[contains(@category, '{category}')]"
        
        # Use ElementTree for XPath queries
        products = root.findall(xpath_expression)
        
        # Process results safely
        result = []
        for product in products:
            # Extract only safe attributes
            product_data = {
                'id': product.get('id', ''),
                'name': product.findtext('name', ''),
                'price': product.findtext('price', '')
            }
            result.append(product_data)
        
        return result

    def _is_safe_category(self, category: str) -> bool:
        """Validate category input to prevent injection"""
        return bool(re.match(r'^[a-zA-Z0-9\s\-]+$', category))

# Example usage
if __name__ == "__main__":
    try:
        query = SecureXMLQuery("products.xml")
        query.load_xml()
        results = query.query_products_by_category("electronics")
        print(results)
    except ValueError as e:
        print(f"Error: {e}")