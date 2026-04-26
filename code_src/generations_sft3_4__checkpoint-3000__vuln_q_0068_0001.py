import xml.etree.ElementTree as ET
tree = ET.parse('file.xml')
root = tree.getroot()

# ===== cell separator =====

import defusedxml.ElementTree as ET
tree = ET.parse('file.xml')
root = tree.getroot()

# ===== cell separator =====

from lxml import etree
tree = etree.parse('file.xml')
root = tree.getroot()

# ===== cell separator =====

from xml.dom import minidom
dom = minidom.parse('file.xml')