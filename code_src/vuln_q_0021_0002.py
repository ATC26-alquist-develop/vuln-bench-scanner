from lxml import etree
from defusedxml.ElementTree import parse
import os

def search_products_by_category(xml_file, category):
    # Validate input
    if not isinstance(xml_file, str) or not isinstance(category, str):
        raise ValueError("Invalid input types")
    
    # Validate XML file path
    if not os.path.exists(xml_file):
        raise FileNotFoundError(f"XML file not found: {xml_file}")
    
    # Parse XML safely using defusedxml
    try:
        tree = parse(xml_file)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML file: {str(e)}")
    
    # Sanitize category input
    safe_category = etree.tostring(etree.Element("category", text=category)).decode('utf-8')
    
    # Construct XPath query
    xpath_query = f".//product[@category='{safe_category}']"
    
    # Execute XPath query
    results = root.xpath(xpath_query)
    
    return results

# Example usage
try:
    xml_file = "products.xml"
    category = "electronics"
    products = search_products_by_category(xml_file, category)
    for product in products:
        print(etree.tostring(product, pretty_print=True).decode('utf-8'))
except Exception as e:
    print(f"Error: {str(e)}")