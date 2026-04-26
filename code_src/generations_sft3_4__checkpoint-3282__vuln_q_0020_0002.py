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
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_model(model_path: str) -> SecureModel:
    """
    Securely load a pre-trained model from a file.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        Loaded and validated model
        
    Raises:
        ValueError: If model loading fails
    """
    try:
        model = SecureModel()
        # Load model state dictionary (assuming it's saved as a .pt file)
        model.load_state_dict(torch.load(model_path))
        model.eval()  # Set model to evaluation mode
        
        # Verify model parameters
        if not all(param.requires_grad == False for param in model.parameters()):
            raise ValueError("Model contains trainable parameters")
            
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

def make_inference(model: SecureModel, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform secure model inference on input data.
    
    Args:
        model: Pre-trained model
        input_data: Dictionary containing input data
        
    Returns:
        Dictionary containing model output
        
    Raises:
        ValueError: If input validation fails
    """
    try:
        # Validate input data
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
            
        # Convert input to tensor
        input_tensor = torch.tensor(input_data['input_data'], dtype=torch.float32)
        
        # Perform inference
        with torch.no_grad():
            output = model(input_tensor)
            
        # Convert output to dictionary
        return {'output_data': output.tolist()}
        
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # Load model
        model = load_model('path/to/model.pt')
        
        # Make inference
        result = make_inference(model, {'input_data': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})
        
        logger.info(f"Inference result: {result}")
        
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")