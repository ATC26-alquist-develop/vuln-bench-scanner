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
        return bool(re.match(r'^[a-zA-Z0-9_\-/]+\.xml$', path))

    def _validate_category(self, category: str) -> bool:
        """Validate category input to prevent injection"""
        return bool(re.match(r'^[a-zA-Z0-9_\-]+$', category))

    def query_products(self, category: str) -> List[Dict[str, str]]:
        """
        Securely query products by category using XPath
        """
        # Validate input
        if not self._validate_category(category):
            raise ValueError("Invalid category format")

        # Parse XML safely
        try:
            self.tree = ET.parse(self.xml_file_path)
        except ET.ParseError:
            raise ValueError("Invalid XML file")

        # Create XPath query
        xpath_query = f"//product[contains(@category, '{category}')]"

        # Execute query safely
        results = self.tree.findall(xpath_query)

        # Process results
        products = []
        for product in results:
            product_dict = {
                "id": product.get("id", ""),
                "name": product.findtext("name", ""),
                "price": product.findtext("price", "")
            }
            products.append(product_dict)

        return products