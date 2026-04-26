from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    xml_data = request.data
    root = ET.fromstring(xml_data)
    # Process the XML data here
    return 'XML processed successfully'

if __name__ == '__main__':
    app.run()