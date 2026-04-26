import os
import cloudpickle
import tempfile
from typing import Any, Optional

def save_model_securely(model: Any, filename: str) -> Optional[str]:
    """
    Securely save a trained model using cloudpickle.
    
    Args:
        model: The trained model to save
        filename: The name of the file to save the model to
    
    Returns:
        The path where the model was saved, or None if saving failed
    """
    try:
        # Create a secure temporary directory
        with tempfile.TemporaryDirectory(prefix='secure_model_') as temp_dir:
            # Construct the full path within the temporary directory
            temp_path = os.path.join(temp_dir, filename)
            
            # Save the model using cloudpickle
            with open(temp_path, 'wb') as f:
                cloudpickle.dump(model, f)
            
            # Return the path to the saved model
            return temp_path
    except (OSError, cloudpickle.pickle.PicklingError) as e:
        # Log the error (implement proper logging in production)
        print(f"Error saving model: {str(e)}")
        return None

def load_model_securely(filepath: str) -> Any:
    """
    Securely load a model saved with cloudpickle.
    
    Args:
        filepath: The path to the saved model file
    
    Returns:
        The loaded model, or None if loading failed
    """
    try:
        # Validate the file path
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        # Check file permissions (should be read-only for the owner)
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"Insufficient permissions to read file: {filepath}")
        
        # Load the model using cloudpickle
        with open(filepath, 'rb') as f:
            return cloudpickle.load(f)
    except (OSError, cloudpickle.pickle.UnpicklingError) as e:
        # Log the error (implement proper logging in production)
        print(f"Error loading model: {str(e)}")
        return None