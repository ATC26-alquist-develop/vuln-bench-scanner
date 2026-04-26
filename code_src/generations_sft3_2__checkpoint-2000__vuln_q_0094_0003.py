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
            
            # Save the model to the temporary file
            with open(temp_path, 'wb') as f:
                cloudpickle.dump(model, f)
            
            # Move the file to the final location
            final_path = os.path.abspath(filename)
            os.replace(temp_path, final_path)
            
        return final_path
    except (OSError, cloudpickle.pickle.PickleError) as e:
        print(f"Error saving model: {str(e)}")
        return None

def load_model_securely(filename: str) -> Optional[Any]:
    """
    Securely load a model saved with cloudpickle.
    
    Args:
        filename: The name of the file containing the model
    
    Returns:
        The loaded model, or None if loading failed
    """
    try:
        # Ensure the file exists and is a regular file
        if not os.path.isfile(filename):
            raise ValueError("Invalid file path")
        
        # Open the file in binary read mode
        with open(filename, 'rb') as f:
            return cloudpickle.load(f)
    except (OSError, cloudpickle.pickle.PickleError) as e:
        print(f"Error loading model: {str(e)}")
        return None