import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
import numpy as np

class SecureModel(nn.Module):
    def __init__(self):
        super(SecureModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(32 * 28 * 28, 10)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Ensure input is on CPU
        if x.device != torch.device('cpu'):
            raise ValueError("Input must be on CPU")
            
        # Add batch dimension if not present
        if len(x.shape) == 2:
            x = x.unsqueeze(0)
            
        # Ensure input is float32
        if x.dtype != torch.float32:
            raise ValueError("Input must be float32")
            
        # Add batch dimension if not present
        if len(x.shape) == 2:
            x = x.unsqueeze(0)
            
        # Add channel dimension if not present
        if len(x.shape) == 3:
            x = x.unsqueeze(1)
            
        # Add batch dimension if not present
        if len(x.shape) == 4:
            x = x.unsqueeze(0)
            
        # Forward pass
        x = F.relu(self.conv1(x))
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x

def secure_inference(model: SecureModel, input_data: np.ndarray) -> np.ndarray:
    """
    Perform secure inference on the model.
    
    Args:
        model: Pre-trained PyTorch model
        input_data: Input data as numpy array
    
    Returns:
        Predictions as numpy array
    """
    # Convert input to PyTorch tensor
    input_tensor = torch.from_numpy(input_data).float()
    
    # Ensure input is on CPU
    if input_tensor.device != torch.device('cpu'):
        raise ValueError("Input must be on CPU")
    
    # Ensure input is float32
    if input_tensor.dtype != torch.float32:
        raise ValueError("Input must be float32")
    
    # Add batch dimension if not present
    if len(input_tensor.shape) == 2:
        input_tensor = input_tensor.unsqueeze(0)
    
    # Add channel dimension if not present
    if len(input_tensor.shape) == 3:
        input_tensor = input_tensor.unsqueeze(1)
    
    # Add batch dimension if not present
    if len(input_tensor.shape) == 4:
        input_tensor = input_tensor.unsqueeze(0)
    
    # Perform inference
    with torch.no_grad():
        output = model(input_tensor)
        
    # Convert output to numpy array
    return output.cpu().numpy()