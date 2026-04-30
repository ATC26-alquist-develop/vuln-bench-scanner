import torch
import torch.nn as nn
from typing import Union, Tuple
import logging

class SecureModelInference:
    def __init__(self, model: nn.Module, device: str = 'cpu'):
        """Initialize secure model inference with input validation."""
        # Validate device
        if device not in ['cpu', 'cuda']:
            raise ValueError("Invalid device. Must be 'cpu' or 'cuda'.")
            
        self.model = model.to(device)
        self.device = device
        self.model.eval()  # Set model to evaluation mode
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_input(self, input_data: Union[torch.Tensor, Tuple[torch.Tensor, ...]]) -> None:
        """Validate input data for secure inference."""
        if not isinstance(input_data, (torch.Tensor, tuple)):
            raise TypeError("Input must be a torch.Tensor or a tuple of torch.Tensors")
            
        if isinstance(input_data, torch.Tensor):
            if input_data.dim() > 3:
                raise ValueError("Input tensor must have 3 or fewer dimensions")
            if input_data.dtype not in [torch.float32, torch.float64]:
                raise ValueError("Input tensor must be float32 or float64")
        elif isinstance(input_data, tuple):
            if not all(isinstance(t, torch.Tensor) for t in input_data):
                raise TypeError("All elements in tuple must be torch.Tensors")
            if not all(t.dim() <= 3 for t in input_data):
                raise ValueError("All tensors in tuple must have 3 or fewer dimensions")
            if not all(t.dtype in [torch.float32, torch.float64] for t in input_data):
                raise ValueError("All tensors in tuple must be float32 or float64")

    def _secure_forward(self, input_data: Union[torch.Tensor, Tuple[torch.Tensor, ...]]) -> torch.Tensor:
        """Perform secure model inference."""
        try:
            self._validate_input(input_data)
            
            # Move input to device
            input_data = input_data.to(self.device)
            
            # Perform inference
            with torch.no_grad():  # Disable gradient calculation
                output = self.model(input_data)
                
            return output.cpu()  # Return result to CPU
            
        except Exception as e:
            self.logger.error(f"Inference error: {str(e)}")
            raise

    def predict(self, input_data: Union[torch.Tensor, Tuple[torch.Tensor, ...]]) -> torch.Tensor:
        """Public method for secure model inference."""
        return self._secure_forward(input_data)