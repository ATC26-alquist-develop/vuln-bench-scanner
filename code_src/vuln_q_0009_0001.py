from flask import Flask, request, jsonify
from defusedxml import ElementTree
import logging
from typing import Dict, Optional

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Ensure the request contains XML data
        if not request.is_xml:
            return jsonify({"error": "Request must be XML"}), 415

        # Parse XML safely using defusedxml
        try:
            xml_data = ElementTree.fromstring(request.data)
        except ElementTree.ParseError as e:
            logger.error(f"Invalid XML: {str(e)}")
            return jsonify({"error": "Invalid XML format"}), 400

        # Process the XML data (example: count elements)
        element_count = len(xml_data.findall(".//*"))

        # Return the result as JSON
        response = {
            "message": "XML processed successfully",
            "element_count": element_count
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error processing XML: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=False)