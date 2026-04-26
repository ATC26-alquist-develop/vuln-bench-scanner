from lxml import etree
import io
import re

def query_products(xml_file, category):
    # Validate input
    if not isinstance(xml_file, str) or not isinstance(category, str):
        raise ValueError("Invalid input types")
    
    # Sanitize inputs
    category = re.sub(r'[^a-zA-Z0-9]', '', category)
    
    try:
        # Parse XML safely
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        # Validate XML structure
        if not root or not root.tag:
            raise ValueError("Invalid XML structure")
        
        # Create XPath query
        xpath_query = f"//product[@category='{category}']"
        
        # Perform query
        results = root.xpath(xpath_query)
        
        # Process results
        products = []
        for product in results:
            # Extract product details safely
            name = product.findtext('name', '')
            price = product.findtext('price', '')
            products.append({
                'name': name,
                'price': price
            })
        
        return products
        
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML syntax: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing XML: {str(e)}")