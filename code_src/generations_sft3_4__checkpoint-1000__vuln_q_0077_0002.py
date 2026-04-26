import json
from typing import Any, Dict

def serialize_data(data: Any) -> str:
    """
    Securely serialize complex data structures to JSON.
    
    Args:
        data: The data to serialize (must be JSON-serializable)
    
    Returns:
        JSON string representation of the data
    """
    if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
        raise ValueError("Unsupported data type for serialization")
    
    return json.dumps(data, default=str)

def deserialize_data(json_str: str) -> Any:
    """
    Securely deserialize JSON data to a Python object.
    
    Args:
        json_str: JSON string to deserialize
    
    Returns:
        Deserialized Python object
    
    Raises:
        ValueError: If the JSON is invalid or contains unsupported types
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise ValueError(f"Deserialization error: {str(e)}")