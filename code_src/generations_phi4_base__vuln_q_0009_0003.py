import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('data.xml')

# Get the root element
root = tree.getroot()

# Iterate through the child elements
for child in root:
    print(child.tag, child.attrib)