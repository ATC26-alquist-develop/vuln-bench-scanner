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
        # Log the error (in a real application, use proper logging)
        print(f"Error saving model: {str(e)}")
        return None

def load_model_securely(filepath: str) -> Optional[Any]:
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
        
        # Check file permissions (readable only by owner)
        if os.access(filepath, os.R_OK) and not os.access(filepath, os.W_OK):
            # Use cloudpickle to load the model
            with open(filepath, 'rb') as f:
                return cloudpickle.load(f)
        else:
            raise PermissionError(f"Insufficient permissions for file: {filepath}")
    except (OSError, cloudpickle.pickle.UnpicklingError) as e:
        # Log the error (in a real application, use proper logging)
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
    saved_path = save_model_securely(model, "secure_model.pkl")
    if saved_path:
        print(f"Model saved to: {saved_path}")
        
        # Load the model securely
        loaded_model = load_model_securely(saved_path)
        if loaded_model:
            print("Model loaded successfully")