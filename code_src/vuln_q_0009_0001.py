from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET
import io

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        # Parse JSON input
        data = request.get_json()
        if not data or 'xml' not in data:
            return jsonify({'error': 'Missing XML data'}), 400

        xml_data = data['xml']

        # Parse XML safely
        try:
            tree = ET.parse(io.StringIO(xml_data))
            root = tree.getroot()
            
            # Process XML data (example: count elements)
            element_count = len(root.findall('.//*'))
            
            return jsonify({'message': f'Processed {element_count} elements'})
            
        except ET.ParseError:
            return jsonify({'error': 'Invalid XML'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False)