import json
from typing import Any, Dict

def serialize_complex_data(data: Any) -> str:
    """
    Securely serialize complex data structures to JSON string.
    
    Args:
        data: The complex data structure to serialize
        
    Returns:
        JSON string representation of the data
        
    Raises:
        TypeError: If data is not serializable
    """
    try:
        return json.dumps(data, default=str)
    except TypeError as e:
        raise TypeError(f"Unable to serialize data: {str(e)}")

def deserialize_complex_data(json_str: str) -> Any:
    """
    Securely deserialize JSON string to complex data structure.
    
    Args:
        json_str: JSON string to deserialize
        
    Returns:
        Deserialized complex data structure
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")