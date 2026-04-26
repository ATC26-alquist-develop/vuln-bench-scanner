import xml.etree.ElementTree as ET

# Function to parse the XML file
def parse_xml_file(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate through each person element
    for person in root.findall('person'):
        name = person.find('name').text
        age = person.find('age').text
        city = person.find('city').text

        # Print the details
        print(f"Name: {name}, Age: {age}, City: {city}")

# Specify the path to the XML file
xml_file_path = 'example.xml'

# Call the function to parse and print the XML data
parse_xml_file(xml_file_path)