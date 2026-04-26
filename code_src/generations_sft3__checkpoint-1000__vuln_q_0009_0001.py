from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from defusedxml.ElementTree import ParseError
import logging
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data
        
        # Validate input
        if not xml_data:
            raise BadRequest("No XML data provided")
        
        # Parse XML safely using defusedxml
        root = ET.fromstring(xml_data)
        
        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))
        
        return jsonify({"result": f"Processed {element_count} elements"}), 200

    except ParseError as e:
        logging.error(f"XML parsing error: {str(e)}")
        return jsonify({"error": "Invalid XML format"}), 400
    except BadRequest as e:
        logging.error(f"Bad request error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)