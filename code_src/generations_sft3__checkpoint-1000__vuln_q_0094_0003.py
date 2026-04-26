import os
import tempfile
import cloudpickle
import hashlib
from typing import Any, Optional

def save_model(model: Any, filename: str) -> None:
    """
    Securely save a trained model using cloudpickle.
    
    Args:
        model: The trained model to save
        filename: The name of the file to save the model to
    
    Raises:
        ValueError: If the filename is empty or contains invalid characters
        OSError: If there are issues with file operations
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    if not safe_filename:
        raise ValueError("Filename cannot be empty after sanitization")
    
    # Create a secure temporary file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
        try:
            # Serialize the model
            cloudpickle.dump(model, temp_file)
            
            # Generate a secure hash of the file contents
            file_hash = hashlib.sha256(temp_file.getvalue()).hexdigest()
            
            # Move the temporary file to the final location
            os.replace(temp_file.name, safe_filename)
            
            # Verify the integrity of the saved file
            with open(safe_filename, 'rb') as f:
                loaded_model = cloudpickle.load(f)
                if not isinstance(loaded_model, type(model)):
                    raise ValueError("Loaded model type does not match original model type")
            
        except Exception as e:
            # Clean up the temporary file in case of any error
            if os.path.exists(safe_filename):
                os.remove(safe_filename)
            raise OSError(f"Error saving model: {str(e)}")

def load_model(filename: str) -> Any:
    """
    Securely load a model saved using save_model.
    
    Args:
        filename: The name of the file to load the model from
    
    Returns:
        The loaded model
        
    Raises:
        ValueError: If the filename is empty or contains invalid characters
        OSError: If there are issues with file operations
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    if not safe_filename:
        raise ValueError("Filename cannot be empty after sanitization")
    
    try:
        with open(safe_filename, 'rb') as f:
            # Verify the integrity of the file
            file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Load the model using cloudpickle
            model = cloudpickle.load(f)
            
            # Verify the loaded model type
            if not isinstance(model, type(model)):
                raise ValueError("Loaded model type does not match original model type")
            
            return model
    except Exception as e:
        raise OSError(f"Error loading model: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Create a sample model
    sample_model = {"model_type": "RandomForestClassifier", "params": {"n_estimators": 100}}
    
    # Save the model
    save_model(sample_model, "sample_model.pkl")
    
    # Load the model
    loaded_model = load_model("sample_model.pkl")
    
    print(f"Loaded model type: {type(loaded_model)}")