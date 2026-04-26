from flask import Flask, request, jsonify
from defusedxml import ElementTree
import io

app = Flask(__name__)

@app.route('/process_xml', methods=['POST'])
def process_xml():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        # Parse JSON data
        data = request.get_json(force=True)
        
        # Validate XML structure
        if not isinstance(data, dict) or 'xml' not in data:
            return jsonify({'error': 'Invalid XML data format'}), 400

        xml_data = data['xml']

        # Parse XML safely
        tree = ElementTree.parse(io.StringIO(xml_data))
        root = tree.getroot()

        # Process XML data (example: count elements)
        element_count = len(root.findall('.//*'))

        return jsonify({'message': f'Processed {element_count} elements successfully'})

    except ElementTree.ParseError:
        return jsonify({'error': 'Invalid XML format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)