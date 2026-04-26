from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from defusedxml.ElementTree import ParseError
import re

app = Flask(__name__)

def validate_xml(xml_string):
    # Check for XML declaration
    if not re.search(r'<\?xml', xml_string):
        return False
    
    # Check for DTD declarations
    if re.search(r'<!DOCTYPE', xml_string):
        return False
    
    # Check for external entity references
    if re.search(r'<!ENTITY', xml_string):
        return False
    
    return True

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data
        
        # Validate XML
        if not validate_xml(xml_data):
            return jsonify({"error": "Invalid XML format"}), 400
        
        # Parse XML safely
        root = ET.fromstring(xml_data)
        
        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))
        
        return jsonify({"count": element_count}), 200
    
    except ParseError:
        return jsonify({"error": "Invalid XML format"}), 400
    except Exception as e:
        # Log the error securely here
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)