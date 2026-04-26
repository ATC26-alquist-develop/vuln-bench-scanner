from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
from defusedxml.ElementTree import ParseError
import logging
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        # Check if XML data is provided
        if not request.is_xml:
            raise BadRequest("XML data is required")

        # Get XML data from request
        xml_data = request.data

        # Validate XML data
        try:
            root = ET.fromstring(xml_data)
        except ParseError as e:
            logging.error(f"XML parsing error: {str(e)}")
            return jsonify({"error": "Invalid XML format"}), 400

        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))
        return jsonify({"count": element_count}), 200

    except BadRequest as e:
        logging.error(f"Bad request error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=False)