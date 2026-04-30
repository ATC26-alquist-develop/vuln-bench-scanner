import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import logging
from typing import Any, Tuple

class SecureModelInference:
    def __init__(self, model: nn.Module, device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        """Initialize secure model inference with proper device handling."""
        self.device = torch.device(device)
        self.model = model.to(self.device)
        self.model.eval()  # Set model to evaluation mode
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_input(self, input_data: Any) -> torch.Tensor:
        """Validate and preprocess input data securely."""
        try:
            # Convert input to tensor and move to device
            input_tensor = torch.tensor(input_data, dtype=torch.float32).to(self.device)
            return input_tensor.unsqueeze(0)  # Add batch dimension
        except Exception as e:
            self.logger.error(f"Invalid input data: {str(e)}")
            raise ValueError("Invalid input data")

    def _secure_forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """Perform secure forward pass with safety checks."""
        try:
            with torch.no_grad():  # Disable gradient calculation for inference
                output = self.model(input_tensor)
            return output
        except Exception as e:
            self.logger.error(f"Error during model inference: {str(e)}")
            raise RuntimeError("Model inference failed")

    def predict(self, input_data: Any) -> torch.Tensor:
        """Perform secure model inference."""
        input_tensor = self._validate_input(input_data)
        output = self._secure_forward(input_tensor)
        return output

# Example usage:
# model = SomePretrainedModel()
# secure_infer = SecureModelInference(model)
# result = secure_infer.predict(input_data)