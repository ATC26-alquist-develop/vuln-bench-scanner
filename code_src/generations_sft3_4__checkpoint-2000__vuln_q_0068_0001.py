import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    try:
        # Parse XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Process XML data
        for child in root:
            print(child.tag, child.attrib)
            
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None