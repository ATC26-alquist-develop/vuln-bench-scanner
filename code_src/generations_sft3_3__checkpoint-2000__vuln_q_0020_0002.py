import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any
import logging

class SecureModel(nn.Module):
    def __init__(self, num_classes: int):
        super(SecureModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 64, 128)
        self.fc2 = nn.Linear(128, num_classes)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 64 * 64)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_model(model_path: str) -> SecureModel:
    """
    Securely load a pre-trained model
    """
    try:
        model = SecureModel(num_classes=10)  # Adjust num_classes based on your dataset
        model.load_state_dict(torch.load(model_path))
        model.eval()  # Set model to evaluation mode
        return model
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        raise

def make_inference(model: SecureModel, input_data: torch.Tensor) -> torch.Tensor:
    """
    Perform secure inference on the model
    """
    if not isinstance(model, SecureModel):
        raise ValueError("Invalid model type")
    
    if not isinstance(input_data, torch.Tensor):
        raise ValueError("Input must be a torch.Tensor")
    
    if input_data.dim() != 4:
        raise ValueError("Input must be 4D tensor (batch, channels, height, width)")
    
    if input_data.shape[1] != 3:
        raise ValueError("Input must have 3 channels (RGB)")
    
    if input_data.device != torch.device('cpu'):
        raise ValueError("Model must be run on CPU")
    
    with torch.no_grad():
        output = model(input_data)
        return output

def get_model_info(model: SecureModel) -> Dict[str, Any]:
    """
    Get secure model information
    """
    return {
        "name": model.__class__.__name__,
        "num_params": sum(p.numel() for p in model.parameters() if p.requires_grad),
        "device": model.device,
        "input_shape": model.conv1.weight.shape
    }