import xml.etree.ElementTree as ET

def read_config_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    config_data = {}
    for child in root:
        config_data[child.tag] = child.text

    return config_data

config_data = read_config_file('config.xml')
print(config_data)