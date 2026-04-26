import torch
import torch.nn as nn
from typing import Tuple
import logging
from pathlib import Path

class SecureModelInference:
    def __init__(self, model_path: str, device: str = 'cpu'):
        """Initialize secure model inference with proper error handling."""
        self.device = torch.device(device)
        self.model = self._load_model(model_path)
        self.model.eval()  # Set model to evaluation mode
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _load_model(self, model_path: str) -> nn.Module:
        """Securely load a pre-trained model."""
        try:
            # Validate path
            path = Path(model_path).resolve()
            if not path.is_file():
                raise ValueError("Model file does not exist")
            
            # Load model
            model = torch.load(model_path, map_location=self.device)
            return model.to(self.device)
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            raise

    def _validate_input(self, input_data: torch.Tensor) -> None:
        """Validate input data."""
        if not isinstance(input_data, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        if input_data.dim() != 4:
            raise ValueError("Input must be a 4D tensor (batch, channels, height, width)")
        if input_data.size(1) != 3:
            raise ValueError("Input must have 3 channels (RGB)")
        if input_data.size(2) < 32 or input_data.size(3) < 32:
            raise ValueError("Input dimensions must be at least 32x32")

    def infer(self, input_data: torch.Tensor) -> torch.Tensor:
        """Perform secure model inference."""
        try:
            # Validate input
            self._validate_input(input_data)

            # Move input to device
            input_data = input_data.to(self.device)

            # Perform inference
            with torch.no_grad():
                output = self.model(input_data)

            return output
        except Exception as e:
            self.logger.error(f"Inference error: {str(e)}")
            raise