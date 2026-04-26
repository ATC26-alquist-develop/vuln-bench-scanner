from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from defusedxml.ElementTree import ParseError
import html

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data
        
        # Validate input
        if not xml_data or not isinstance(xml_data, bytes):
            return jsonify({"error": "Invalid input"}), 400
            
        # Sanitize input
        xml_data = html.escape(xml_data.decode('utf-8'))
        
        # Parse XML safely using defusedxml
        root = ET.fromstring(xml_data)
        
        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))
        
        return jsonify({"count": element_count}), 200
        
    except ParseError:
        return jsonify({"error": "Invalid XML format"}), 400
    except Exception as e:
        # Avoid exposing sensitive error details
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)