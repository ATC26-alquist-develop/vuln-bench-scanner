import xml.etree.ElementTree as ET
from io import StringIO

def parse_xml(xml_string):
    try:
        tree = ET.parse(StringIO(xml_string))
        root = tree.getroot()
        # Process the XML data here
        return root
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return None

# ===== cell separator =====

from lxml import etree

def parse_xml_lxml(xml_string):
    try:
        tree = etree.fromstring(xml_string)
        # Process the XML data here
        return tree
    except etree.XMLSyntaxError as e:
        print(f"XML parsing error: {e}")
        return None

# ===== cell separator =====

import defusedxml.ElementTree as ET

def parse_xml_defused(xml_string):
    try:
        tree = ET.parse(StringIO(xml_string))
        root = tree.getroot()
        # Process the XML data here
        return root
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return None