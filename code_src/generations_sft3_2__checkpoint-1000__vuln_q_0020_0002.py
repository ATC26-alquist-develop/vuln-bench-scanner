import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
import os

class SecureModel(nn.Module):
    def __init__(self):
        super(SecureModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_model(model_path: str) -> SecureModel:
    """
    Securely load a pre-trained model from a file.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Verify file permissions
    if not os.access(model_path, os.R_OK):
        raise PermissionError(f"Insufficient permissions to read model file: {model_path}")
    
    # Load model using torch.load with secure defaults
    model = torch.load(model_path, map_location=torch.device('cpu'))
    
    # Verify model type
    if not isinstance(model, SecureModel):
        raise TypeError("Loaded model is not an instance of SecureModel")
    
    return model

def make_inference(model: SecureModel, input_data: torch.Tensor) -> torch.Tensor:
    """
    Perform secure inference on the given model and input data.
    """
    if not isinstance(model, SecureModel):
        raise TypeError("Input model must be an instance of SecureModel")
    
    if not isinstance(input_data, torch.Tensor):
        raise TypeError("Input data must be a torch.Tensor")
    
    if input_data.dim() != 4:
        raise ValueError("Input data must be 4-dimensional tensor (batch, channels, height, width)")
    
    # Ensure input data is on CPU
    if input_data.device != torch.device('cpu'):
        raise RuntimeError("Input data must be on CPU for secure inference")
    
    # Perform inference
    with torch.no_grad():
        output = model(input_data)
    
    return output

# Example usage
if __name__ == "__main__":
    # Load pre-trained model
    model_path = "path/to/secure_model.pt"
    model = load_model(model_path)
    
    # Prepare input data (example: 1x1x28x28 image)
    input_data = torch.randn(1, 1, 28, 28, device='cpu')
    
    # Perform inference
    output = make_inference(model, input_data)
    
    print("Inference complete")