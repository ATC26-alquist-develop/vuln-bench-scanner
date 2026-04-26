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
    
    # Create a temporary file for initial write
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
        try:
            # Serialize the model
            cloudpickle.dump(model, temp_file)
            
            # Get the hash of the serialized data
            serialized_data = temp_file.getvalue()
            model_hash = hashlib.sha256(serialized_data).hexdigest()
            
            # Write the hash to a separate file
            hash_filename = f"{safe_filename}.hash"
            with open(hash_filename, 'w') as hash_file:
                hash_file.write(model_hash)
            
            # Rename the temporary file to the final filename
            os.rename(temp_file.name, filename)
            
        except Exception as e:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            raise OSError(f"Error saving model: {str(e)}")

def load_model(filename: str) -> Any:
    """
    Securely load a model saved with cloudpickle.
    
    Args:
        filename: The name of the file to load the model from
    
    Returns:
        The loaded model
        
    Raises:
        ValueError: If the filename is empty or contains invalid characters
        OSError: If there are issues with file operations
        RuntimeError: If the model hash verification fails
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    if not safe_filename:
        raise ValueError("Filename cannot be empty after sanitization")
    
    # Verify the integrity of the file
    hash_filename = f"{safe_filename}.hash"
    if not os.path.exists(hash_filename):
        raise OSError(f"Hash file {hash_filename} not found")
    
    try:
        with open(hash_filename, 'r') as hash_file:
            expected_hash = hash_file.read().strip()
        
        with open(filename, 'rb') as model_file:
            serialized_data = model_file.read()
            actual_hash = hashlib.sha256(serialized_data).hexdigest()
        
        if actual_hash != expected_hash:
            raise RuntimeError("Model integrity check failed")
        
        # Deserialize the model
        return cloudpickle.load(model_file)
    
    except Exception as e:
        raise OSError(f"Error loading model: {str(e)}")