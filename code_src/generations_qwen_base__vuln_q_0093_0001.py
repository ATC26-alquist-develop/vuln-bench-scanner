import xml.etree.ElementTree as ET

# ===== cell separator =====

# Sample XML data
xml_data = '''
<root>
    <person>
        <name>John Doe</name>
        <age>30</age>
        <city>New York</city>
    </person>
    <person>
        <name>Jane Doe</name>
        <age>25</age>
        <city>Los Angeles</city>
    </person>
</root>
'''

# Parse the XML data
tree = ET.ElementTree(ET.fromstring(xml_data))

# ===== cell separator =====

root = tree.getroot()

# ===== cell separator =====

persons = root.findall('person')
for person in persons:
    name = person.find('name').text
    age = person.find('age').text
    city = person.find('city').text
    print(f"Name: {name}, Age: {age}, City: {city}")

# ===== cell separator =====

for person in persons:
    name = person.find('name').text
    age = person.find('age').attrib['value']  # Assuming 'value' is the attribute name
    city = person.find('city').text
    print(f"Name: {name}, Age: {age}, City: {city}")

# ===== cell separator =====

new_person = ET.Element('person')
new_name = ET.SubElement(new_person, 'name')
new_name.text = 'Alice'
new_age = ET.SubElement(new_person, 'age')
new_age.text = '28'
new_city = ET.SubElement(new_person, 'city')
new_city.text = 'Chicago'

# Append the new person to the root
root.append(new_person)

# Create a new XML tree and write it to a file
new_tree = ET.ElementTree(root)
new_tree.write('new_data.xml')

# ===== cell separator =====

try:
    root = tree.getroot()
    persons = root.findall('person')
    for person in persons:
        name = person.find('name').text
        age = person.find('age').text
        city = person.find('city').text
        print(f"Name: {name}, Age: {age}, City: {city}")
except AttributeError as e:
    print(f"Error: {e}")

# ===== cell separator =====

with open('data.xml', 'r') as file:
    xml_data = file.read()
tree = ET.ElementTree(ET.fromstring(xml_data))