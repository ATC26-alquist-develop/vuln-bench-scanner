import xml.etree.ElementTree as ET

def read_config_from_xml(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract configuration data
    config_data = {}
    for setting in root.findall('setting'):
        name = setting.get('name')
        value = setting.text
        config_data[name] = value

    return config_data

# Path to the XML file
xml_file_path = 'app_config.xml'

# Read and print the configuration data
config_data = read_config_from_xml(xml_file_path)
print(config_data)

# ===== cell separator =====

{
    'app_name': 'MyApp',
    'version': '1.0.0',
    'database': {
        'host': 'localhost',
        'port': '3306',
        'user': 'root',
        'password': 'password'
    },
    'log_level': 'INFO'
}