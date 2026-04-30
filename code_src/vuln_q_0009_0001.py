from flask import Flask, request, jsonify
from defusedxml.ElementTree import fromstring
import html

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        xml_data = request.get_json().get('xml', '')
        if not xml_data:
            return jsonify({"error": "No XML data provided"}), 400

        # Parse XML safely using defusedxml
        root = fromstring(xml_data)
        
        # Process the XML data here
        # Example: Extracting text from all elements
        processed_data = []
        for elem in root.iter():
            processed_data.append(html.escape(elem.text.strip() if elem.text else ''))

        return jsonify({"result": processed_data}), 200

    except ValueError:
        return jsonify({"error": "Invalid XML data"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the XML"}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development