import xml.etree.ElementTree as ET

# Sample XML data
xml_data = """<root>
    <child name="child1">Content 1</child>
    <child name="child2">Content 2</child>
</root>"""

# Parse the XML data
root = ET.fromstring(xml_data)

# Iterate over child elements and print their content
for child in root:
    print(f"Name: {child.attrib['name']}, Content: {child.text}")