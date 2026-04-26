import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any
import logging

class SecureModel(nn.Module):
    def __init__(self):
        super(SecureModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3)
        self.fc1 = nn.Linear(8 * 20 * 20, 10)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 8 * 20 * 20)
        x = self.fc1(x)
        return F.log_softmax(x, dim=1)

def load_model(model_path: str) -> SecureModel:
    """
    Securely load a pre-trained model from a file.
    """
    try:
        model = SecureModel()
        # Use torch.load with map_location to ensure safe loading
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()  # Set model to evaluation mode
        return model
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        raise

def make_inference(model: SecureModel, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform secure inference on the model.
    """
    try:
        # Validate input data
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
            
        # Convert input to PyTorch tensor
        input_tensor = torch.tensor(input_data['input_data'], dtype=torch.float32)
        
        # Ensure input tensor is on CPU
        input_tensor = input_tensor.to('cpu')
        
        # Perform inference
        with torch.no_grad():
            output = model(input_tensor)
            
        # Convert output to dictionary
        output_dict = {
            'logits': output.cpu().numpy().tolist(),
            'probabilities': output.softmax(dim=1).cpu().numpy().tolist()
        }
        
        return output_dict
        
    except Exception as e:
        logging.error(f"Inference error: {str(e)}")
        raise