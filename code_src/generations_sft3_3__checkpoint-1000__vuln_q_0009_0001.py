from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re

app = Flask(__name__)

def validate_xml(xml_string):
    # Validate XML structure
    try:
        root = ET.fromstring(xml_string)
        # Add more specific validation rules here
        return True
    except ET.ParseError:
        return False

def sanitize_input(input_string):
    # Remove any potentially harmful characters
    return re.sub(r'[^\w\s-]', '', input_string)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data
        
        # Validate XML
        if not validate_xml(xml_data):
            return jsonify({"error": "Invalid XML"}), 400

        # Sanitize input
        sanitized_xml = sanitize_input(xml_data.decode('utf-8'))

        # Parse XML safely
        root = parse(sanitized_xml)

        # Process XML data here
        # ...

        return jsonify({"message": "XML processed successfully"}), 200

    except Exception as e:
        # Log the error securely (not implemented here)
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production