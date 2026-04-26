import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any
import logging

class SecureModel(nn.Module):
    def __init__(self, state_dict_path: str):
        """Initialize model with secure loading of pre-trained weights."""
        super().__init__()
        self.model = torch.load(state_dict_path)
        self.model.eval()  # Set model to evaluation mode
        
        # Verify model structure
        self._verify_model_structure()

    def _verify_model_structure(self) -> None:
        """Verify model structure matches expected structure."""
        expected_keys = {'layer1', 'layer2', 'classifier'}
        loaded_keys = set(self.model.state_dict().keys())
        if not expected_keys.issubset(loaded_keys):
            raise ValueError("Model structure mismatch")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with input validation."""
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        
        if x.dim() != 4:
            raise ValueError("Input must be 4-dimensional tensor")
            
        return self.model(x)

def load_model(model_path: str) -> SecureModel:
    """Securely load model with validation."""
    if not isinstance(model_path, str):
        raise TypeError("Model path must be a string")
        
    if not torch.cuda.is_available():
        return SecureModel(model_path)
    else:
        return SecureModel(model_path).cuda()

def make_inference(model: SecureModel, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Make inference with input validation."""
    if not isinstance(model, SecureModel):
        raise TypeError("Invalid model type")
        
    if not isinstance(input_data, dict):
        raise TypeError("Input must be a dictionary")
        
    # Validate input data
    required_keys = {'input_tensor'}
    if not required_keys.issubset(input_data.keys()):
        raise ValueError("Missing required input keys")
        
    if not isinstance(input_data['input_tensor'], torch.Tensor):
        raise TypeError("Input tensor must be a torch.Tensor")
        
    # Perform inference
    with torch.no_grad():
        output = model(input_data['input_tensor'])
        
    # Convert to numpy for safe return
    return {'output': output.cpu().numpy()}