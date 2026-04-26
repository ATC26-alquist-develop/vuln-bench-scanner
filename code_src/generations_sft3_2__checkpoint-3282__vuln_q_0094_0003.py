import os
import cloudpickle
import tempfile
from typing import Any, Optional

def save_model_securely(model: Any, filename: str) -> Optional[str]:
    """
    Securely save a model using cloudpickle with proper error handling.
    
    Args:
        model: The model object to save
        filename: The name of the file to save the model to
    
    Returns:
        str: Path to the saved file if successful, None if failed
    """
    try:
        # Create a secure temporary directory
        with tempfile.TemporaryDirectory(prefix='secure_model_') as temp_dir:
            # Construct the full path within the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            
            # Save the model using cloudpickle
            with open(temp_file_path, 'wb') as f:
                cloudpickle.dump(model, f)
            
            # Return the full path to the saved file
            return temp_file_path
    except Exception as e:
        # Log the error (in a production environment, use proper logging)
        print(f"Error saving model: {str(e)}")
        return None

def load_model_securely(file_path: str) -> Any:
    """
    Securely load a model using cloudpickle with proper error handling.
    
    Args:
        file_path: Path to the saved model file
    
    Returns:
        Any: The loaded model object
    """
    try:
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file permissions
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"No read permission for file: {file_path}")
        
        # Load the model using cloudpickle
        with open(file_path, 'rb') as f:
            return cloudpickle.load(f)
    except Exception as e:
        # Log the error (in a production environment, use proper logging)
        print(f"Error loading model: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Assume we have a trained model
    from sklearn.ensemble import RandomForestClassifier
    
    # Create a sample model
    model = RandomForestClassifier()
    model.fit([[0, 0], [0, 0], [1, 1], [1, 1]], [[0], [1], [1], [0]])
    
    # Save the model securely
    saved_path = save_model_securely(model, "my_model.pkl")
    if saved_path:
        print(f"Model saved to: {saved_path}")
        
        # Load the model securely
        loaded_model = load_model_securely(saved_path)
        if loaded_model:
            print("Model loaded successfully")
    else:
        print("Failed to save or load model")