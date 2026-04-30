```python
import torch
import torch.nn as nn
from typing import Tuple
import logging
from pathlib import Path

class SecureModelInference:
    def __init__(self, model_path: str, device: str = 'cpu'):
        """
        Initialize secure model inference with validation.
        
        Args:
            model_path: Path to the pre-trained model
            device: Device to run inference on ('cpu' or 'cuda')
        """
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate and set device
        if device not in ['cpu', 'cuda']:
            raise ValueError("Device must be 'cpu' or 'cuda'")
        self.device = torch.device(device)
        
        # Load model securely
        try:
            self.model = self._load_model(model_path)
            self.model.eval()  # Set model to evaluation mode
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise

    def _load_model(self, model_path: str) -> nn.Module:
        """
        Securely load the model from file.
        """
        # Validate path
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load model with strict type checking
        try:
            model = torch.load(path, map_location=self.device)
            if not isinstance(model, nn.Module):
                raise TypeError("Loaded object is not a PyTorch model")
            return model
        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")

    def _validate_input(self, input_data: torch.Tensor) -> None:
        """
        Validate input data before inference.
        """
        if not isinstance(input_data, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        
        if input_data.dim() < 2:
            raise ValueError("Input must be at least 2D")
        
        if input_data.size(0) == 0:
            raise ValueError("Input batch size must be greater than 0")

    def infer(self, input_data: torch.Tensor) -> torch.Tensor:
        """
        Perform secure model inference.
        
        Args:
            input_data: Input tensor for inference
            
        Returns:
            Output tensor from model
        """
        # Validate input
        self._validate_input(input_data)
        
        # Move input to device
        input_data = input_data.to(self.device)
        
        # Perform inference with context manager
        with torch.no_grad():  # Disable gradient calculation for inference
            try:
                output = self.model(input_data)
                return output
            except Exception as e:
                self.logger.error(f"Inference error: {str(e)}")
                raise

# Example usage:
if __name__ == "__main__":
    try:
        # Initialize with CPU
        # model_path = 'path/to/pretrained/model.pth'
        # inference = SecureModelInference(model_path)
        # result = inference.infer(input_data)
        # print(result)
        pass
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
```