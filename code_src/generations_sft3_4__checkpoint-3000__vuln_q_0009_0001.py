from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from io import StringIO
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
            
        # Parse XML safely using defusedxml
        tree = ET.parse(StringIO(xml_data.decode('utf-8')))
        root = tree.getroot()
        
        # Process XML data
        # Example: Extract and validate some elements
        name = root.find('name')
        if name is not None:
            name_text = name.text
            if name_text and len(name_text) > 0:
                # Sanitize output
                safe_name = html.escape(name_text)
                return jsonify({"name": safe_name})
            else:
                return jsonify({"error": "Invalid name element"}), 400
        else:
            return jsonify({"error": "Missing name element"}), 400

    except ET.ParseError:
        return jsonify({"error": "Invalid XML format"}), 400
    except Exception as e:
        # Avoid exposing sensitive error details
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production