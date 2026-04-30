import cloudpickle
import os
from typing import Any

def save_model(model: Any, filename: str) -> None:
    """Securely save a model using cloudpickle."""
    # Validate filename to prevent path traversal
    if not os.path.abspath(filename).startswith(os.getcwd()):
        raise ValueError("Invalid filename - must be within current directory")
    
    # Ensure the file has a .pkl extension
    if not filename.endswith('.pkl'):
        filename += '.pkl'
    
    # Securely write the model to file
    with open(filename, 'wb') as f:
        cloudpickle.dump(model, f)

def load_model(filename: str) -> Any:
    """Securely load a model using cloudpickle."""
    # Validate filename to prevent path traversal
    if not os.path.abspath(filename).startswith(os.getcwd()):
        raise ValueError("Invalid filename - must be within current directory")
    
    # Ensure the file has a .pkl extension
    if not filename.endswith('.pkl'):
        filename += '.pkl'
    
    # Securely read the model from file
    with open(filename, 'rb') as f:
        return cloudpickle.load(f)