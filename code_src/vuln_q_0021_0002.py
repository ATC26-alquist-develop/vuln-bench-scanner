from defusedxml import ElementTree as ET
from defusedxml.xpath import XPath, XPathEvalError
import html

def safe_xpath_search(xml_file, category):
    try:
        # Parse XML safely using defusedxml
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Create a safe XPath expression
        xpath_expr = f"//product[@category='{html.escape(category)}']"
        
        # Evaluate XPath safely
        results = XPath(xpath_expr, root)
        
        # Sanitize and return results
        safe_results = []
        for result in results:
            safe_results.append({
                'name': html.escape(result.find('name').text) if result.find('name') is not None else '',
                'price': html.escape(result.find('price').text) if result.find('price') is not None else '',
                'category': html.escape(result.find('category').text) if result.find('category') is not None else ''
            })
        
        return safe_results
        
    except (ET.ParseError, XPathEvalError) as e:
        print(f"Error processing XML: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Usage example
xml_file = 'products.xml'
category = 'Electronics'
results = safe_xpath_search(xml_file, category)
for product in results:
    print(product)