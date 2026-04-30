import cloudpickle
import os
from typing import Any

def save_data(data: Any, filename: str) -> None:
    """Securely save data to a file using cloudpickle."""
    # Validate filename to prevent path traversal
    if not os.path.isabs(filename):
        raise ValueError("Filename must be an absolute path")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Serialize and save data
    with open(filename, 'wb') as f:
        cloudpickle.dump(data, f)

def load_data(filename: str) -> Any:
    """Securely load data from a file using cloudpickle."""
    # Validate filename to prevent path traversal
    if not os.path.isabs(filename):
        raise ValueError("Filename must be an absolute path")
    
    # Ensure the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    # Deserialize and return data
    with open(filename, 'rb') as f:
        return cloudpickle.load(f)

# Example usage
if __name__ == "__main__":
    # Save data
    data_to_save = {"key": "value", "list": [1, 2, 3], "nested": {"a": 1}}
    save_data(data_to_save, "/path/to/secure/location/data.pkl")
    
    # Load data
    loaded_data = load_data("/path/to/secure/location/data.pkl")
    print(loaded_data)