from defusedxml import ElementTree as ET

def parse_xml_safely(xml_string):
    try:
        root = ET.fromstring(xml_string)
        # Process XML data here
        return root
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return None

# ===== cell separator =====

import xml.etree.ElementTree as ET

def parse_xml_safely(xml_string):
    try:
        root = ET.fromstring(xml_string)
        # Process XML data here
        return root
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return None