import os
import cloudpickle
import hashlib
from typing import Any

class SecureModelSaver:
    def __init__(self, model: Any, output_dir: str):
        """
        Initialize the secure model saver with a trained model and output directory.
        
        Args:
            model: The trained machine learning model to save.
            output_dir: The directory where the model will be saved.
        """
        self.model = model
        self.output_dir = output_dir
        self._validate_output_dir()

    def _validate_output_dir(self) -> None:
        """Validate and create the output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        elif not os.path.isdir(self.output_dir):
            raise ValueError("Output path must be a directory")

    def _generate_secure_filename(self) -> str:
        """Generate a secure filename using a hash of the model's state."""
        model_hash = hashlib.sha256(str(self.model).encode()).hexdigest()
        return f"{model_hash}.pkl"

    def save_model(self) -> None:
        """Securely save the model using cloudpickle."""
        filename = self._generate_secure_filename()
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'wb') as f:
                cloudpickle.dump(self.model, f)
        except Exception as e:
            raise RuntimeError(f"Failed to save model: {str(e)}")

    def load_model(self) -> Any:
        """Securely load a model from a file."""
        filename = self._generate_secure_filename()
        filepath = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        try:
            with open(filepath, 'rb') as f:
                return cloudpickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")

# Example usage:
# model = ... # Your trained machine learning model
# saver = SecureModelSaver(model, '/path/to/output/directory')
# saver.save_model()
# loaded_model = saver.load_model()