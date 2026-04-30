import defusedxml.ElementTree as ET
from typing import Optional
import re

def validate_category(category: str) -> bool:
    """Validate that the category contains only allowed characters."""
    # Only allow letters, spaces, and common punctuation
    return bool(re.match(r'^[a-zA-Z\s\-\.]+$', category))

def search_products(xml_path: str, category: str) -> Optional[str]:
    """
    Securely search for products in an XML file by category.
    
    Args:
        xml_path: Path to the XML file
        category: Category to search for
        
    Returns:
        Product information as a string or None if not found
    """
    # Validate inputs
    if not validate_category(category):
        raise ValueError("Invalid category format")
    
    if not xml_path or not isinstance(xml_path, str):
        raise ValueError("Invalid XML path")

    try:
        # Parse XML securely using defusedxml
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find products in the specified category
        for product in root.findall('.//product'):
            if product.find('category').text.lower() == category.lower():
                # Return product information safely
                name = product.find('name').text if product.find('name') is not None else "N/A"
                price = product.find('price').text if product.find('price') is not None else "N/A"
                return f"Product: {name}, Price: {price}"
        
        return None

    except (ET.ParseError, FileNotFoundError, PermissionError) as e:
        # Log the error securely here if needed
        return None