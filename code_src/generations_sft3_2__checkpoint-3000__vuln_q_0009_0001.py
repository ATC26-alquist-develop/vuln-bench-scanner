from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from werkzeug.exceptions import BadRequest
import html

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data
        
        # Validate input
        if not xml_data:
            raise BadRequest("No XML data provided")
        
        # Sanitize input
        xml_data = html.escape(xml_data.decode('utf-8'))
        
        # Parse XML safely using defusedxml
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError:
            raise BadRequest("Invalid XML format")
        
        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))
        
        return jsonify({"message": "XML processed successfully", "element_count": element_count})
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Avoid exposing sensitive information in error messages
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production