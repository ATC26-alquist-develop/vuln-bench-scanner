import xml.etree.ElementTree as ET

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for child in root:
        print(child.tag, child.attrib)

if __name__ == '__main__':
    parse_xml('example.xml')