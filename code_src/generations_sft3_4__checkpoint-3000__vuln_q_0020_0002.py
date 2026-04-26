import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureModel(nn.Module):
    def __init__(self):
        super(SecureModel, self).__init__()
        self.fc1 = nn.Linear(10, 16)
        self.fc2 = nn.Linear(16, 10)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Ensure input is on CPU
        if x.device.type != 'cpu':
            logger.warning("Input tensor is on GPU. Moving to CPU for security.")
            x = x.to('cpu')
            
        # Apply activation function
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_model(model_path: str) -> SecureModel:
    """
    Securely load a PyTorch model
    """
    try:
        model = SecureModel()
        # Load model state dictionary
        checkpoint = torch.load(model_path, map_location='cpu')
        model.load_state_dict(checkpoint['model_state_dict'])
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def make_inference(model: SecureModel, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform secure inference on the model
    """
    try:
        # Validate input data
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
            
        # Move input to CPU
        if next(model.parameters()).is_cuda:
            logger.warning("Model is on GPU. Moving input to CPU for security.")
            input_data = {k: v.to('cpu') for k, v in input_data.items()}
            
        # Ensure input is a tensor
        if not isinstance(input_data.get('input'), torch.Tensor):
            raise ValueError("Input must be a tensor")
            
        # Perform inference
        with torch.no_grad():
            output = model(input_data['input'])
            
        # Convert output to dictionary
        return {'output': output.cpu().numpy()}
        
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        raise