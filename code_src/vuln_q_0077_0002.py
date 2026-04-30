import json
import base64

def serialize_data(data):
    """Serialize complex data structures to JSON and encode as base64."""
    json_data = json.dumps(data)
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    return encoded_data

def deserialize_data(encoded_data):
    """Decode base64 and deserialize JSON to Python object."""
    decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
    data = json.loads(decoded_data)
    return data