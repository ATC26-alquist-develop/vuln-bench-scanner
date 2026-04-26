import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Process the XML data
        for child in root:
            print(f"{child.tag}: {child.text}")
            
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
parse_xml("example.xml")