from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    # Get the XML data from the request
    xml_data = request.data.decode('utf-8')
    
    # Parse the XML data
    root = ET.fromstring(xml_data)
    
    # Extract data from the XML (example: assume the XML has a root element with a 'name' tag)
    name = root.find('name').text
    
    # Process the data (example: just return the name)
    processed_data = {'name': name}
    
    # Return the processed data in XML format
    response = ET.Element('response')
    ET.SubElement(response, 'name').text = name
    return ET.tostring(response, encoding='utf-8', method='xml').decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)