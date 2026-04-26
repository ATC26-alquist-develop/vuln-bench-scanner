import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('example.xml')

# Get the root element
root = tree.getroot()

# Iterate over elements
for child in root:
    print(child.tag, child.attrib)

# ===== cell separator =====

from lxml import etree

# Parse the XML file
tree = etree.parse('example.xml')

# Get the root element
root = tree.getroot()

# Iterate over elements
for child in root:
    print(child.tag, child.attrib)