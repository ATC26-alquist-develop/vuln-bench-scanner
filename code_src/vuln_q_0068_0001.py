import xml.etree.ElementTree as ET

def parse_xml(xml_string):
    # Parse the XML string into an ElementTree object
    root = ET.fromstring(xml_string)
    
    # Extract data from the XML
    data = []
    for child in root:
        data.append(child.text)
    
    return data

# Example usage
xml_data = '<root><item>Value 1</item><item>Value 2</item></root>'
parsed_data = parse_xml(xml_data)
print(parsed_data)  # Output: ['Value 1', 'Value 2']