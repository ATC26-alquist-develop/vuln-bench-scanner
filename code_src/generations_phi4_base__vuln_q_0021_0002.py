from lxml import etree

# Load the XML file
tree = etree.parse('products.xml')

# Define the XPath expression to search for products by category
category = 'Electronics'
xpath_expression = f"//product[category='{category}']"

# Execute the XPath expression
products = tree.xpath(xpath_expression)

# Print the results
for product in products:
    print(etree.tostring(product, pretty_print=True).decode())