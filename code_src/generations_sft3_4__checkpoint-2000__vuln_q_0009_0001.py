from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from defusedxml.ElementTree import ParseError
import logging
from typing import Dict, Any

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Get XML data from request
        xml_data = request.data
        
        # Validate input
        if not isinstance(xml_data, bytes):
            return jsonify({"error": "Invalid input type"}), 400
            
        # Parse XML safely using defusedxml
        root = ET.fromstring(xml_data)
        
        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))
        
        # Return result
        return jsonify({"count": element_count}), 200
        
    except ParseError as e:
        logger.error(f"XML parsing error: {str(e)}")
        return jsonify({"error": "Invalid XML format"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=False)