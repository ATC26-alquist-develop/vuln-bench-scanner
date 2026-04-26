import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('example.xml')

# Get the root element of the XML
root = tree.getroot()

# Iterate over all child elements of the root
for child in root:
    print(f"Tag: {child.tag}, Text: {child.text}")

# ===== cell separator =====

import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('example.xml')

# Get the root element of the XML
root = tree.getroot()

# Iterate over all child elements of the root
for item in root.findall('items/item'):
    # Print the tag and text of each 'item' element
    print(f"Tag: {item.tag}, Text: {item.text}")
    
    # Iterate over all child elements of the 'item' element
    for subitem in item:
        print(f"Subtag: {subitem.tag}, Subtext: {subitem.text}")

# ===== cell separator =====

import xml.etree.ElementTree as ET

xml_data = '''
<root>
    <item id="1">
        <name>Item 1</name>
        <description>First item description</description>
    </item>
    <item id="2">
        <name>Item 2</name>
        <description>Second item description</description>
    </item>
</root>
'''

# Parse the XML string
root = ET.fromstring(xml_data)

# Iterate over all child elements of the root
for item in root.findall('item'):
    print(f"Tag: {item.tag}, Text: {item.text}")
    
    # Iterate over all child elements of the 'item' element
    for subitem in item:
        print(f"Subtag: {subitem.tag}, Subtext: {subitem.text}")

# ===== cell separator =====

import xml.etree.ElementTree as ET

try:
    tree = ET.parse('example.xml')
    root = tree.getroot()
    # Your parsing logic here
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")
except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")