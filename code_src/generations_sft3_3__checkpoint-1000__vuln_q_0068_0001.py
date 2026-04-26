import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Process the XML data
        for child in root:
            print(f"Tag: {child.tag}, Text: {child.text}")
            
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None