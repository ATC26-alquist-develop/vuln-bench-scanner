import os
import tempfile
import cloudpickle
import hashlib
from typing import Any

def save_model_securely(model: Any, filename: str) -> None:
    """
    Securely save a trained model using cloudpickle.
    
    Args:
        model: The trained model to save
        filename: The name of the file to save the model to
    """
    # Create a secure temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a unique filename using a hash of the original filename
        original_filename = os.path.basename(filename)
        unique_filename = hashlib.sha256(original_filename.encode()).hexdigest()
        temp_filename = os.path.join(temp_dir, unique_filename)
        
        try:
            # Save the model to the temporary file
            with open(temp_filename, 'wb') as f:
                cloudpickle.dump(model, f)
            
            # Move the file to the final location
            os.replace(temp_filename, filename)
        except Exception as e:
            # If any error occurs, remove the temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            raise e

def load_model_securely(filename: str) -> Any:
    """
    Securely load a model saved using save_model_securely.
    
    Args:
        filename: The name of the file containing the model
        
    Returns:
        The loaded model
    """
    try:
        with open(filename, 'rb') as f:
            return cloudpickle.load(f)
    except Exception as e:
        raise ValueError(f"Failed to load model: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Create a sample model
    sample_model = {"model": "dummy"}
    
    # Save the model
    save_model_securely(sample_model, "sample_model.pkl")
    
    # Load the model
    loaded_model = load_model_securely("sample_model.pkl")
    
    print("Model loaded successfully:", loaded_model)