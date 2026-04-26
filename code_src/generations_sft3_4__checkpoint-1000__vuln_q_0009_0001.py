from flask import Flask, request, jsonify
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError
import re

app = Flask(__name__)

def validate_xml(xml_string):
    # Basic validation to ensure XML is well-formed
    try:
        ET.fromstring(xml_string)
        return True
    except ParseError:
        return False

def sanitize_input(xml_string):
    # Remove any potentially harmful characters
    return re.sub(r'[^\w\s<>\-]', '', xml_string)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data.decode('utf-8')
        
        # Validate XML
        if not validate_xml(xml_data):
            return jsonify({"error": "Invalid XML"}), 400
        
        # Sanitize input
        sanitized_xml = sanitize_input(xml_data)
        
        # Process XML (example: count elements)
        root = ET.fromstring(sanitized_xml)
        element_count = len(root.findall('.//*'))
        
        return jsonify({"count": element_count}), 200
    
    except Exception as e:
        # Log the error securely (not implemented here)
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production