import json
from typing import Any, Dict
import os

class SecureJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return {'__class__': 'bytes', 'value': obj.decode('utf-8')}
        return super().default(obj)

class SecureJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '__class__' in obj and obj['__class__'] == 'bytes':
            return obj['value'].encode('utf-8')
        return obj

def save_data(data: Dict[str, Any], filename: str) -> None:
    """
    Securely save complex data structures to a JSON file.
    
    Args:
        data: Dictionary containing the data to save
        filename: Name of the file to save to
    """
    try:
        # Ensure the filename is safe
        safe_filename = os.path.basename(filename)
        if not safe_filename.endswith('.json'):
            safe_filename += '.json'
        
        # Serialize data
        json_data = json.dumps(data, cls=SecureJSONEncoder)
        
        # Write to file securely
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(json_data)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"Error saving data: {str(e)}")

def load_data(filename: str) -> Dict[str, Any]:
    """
    Securely load data from a JSON file.
    
    Args:
        filename: Name of the file to load from
        
    Returns:
        Dictionary containing the loaded data
    """
    try:
        # Ensure the filename is safe
        safe_filename = os.path.basename(filename)
        if not safe_filename.endswith('.json'):
            raise ValueError("Invalid filename. Must end with .json")
        
        # Read from file securely
        with open(safe_filename, 'r', encoding='utf-8') as f:
            json_data = f.read()
        
        # Parse JSON data securely
        data = json.loads(json_data, cls=SecureJSONDecoder)
        
        return data
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading data: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Example data
    data = {
        "name": "John Doe",
        "age": 30,
        "preferences": {"color": "blue", "food": "pizza"}
    }
    
    # Save data
    save_data(data, "user_data.json")
    
    # Load data
    loaded_data = load_data("user_data.json")
    print("Loaded data:", loaded_data)