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

def load_model(model_path: str) -> nn.Module:
    """
    Securely load a pre-trained PyTorch model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Verify file permissions
    if not os.access(model_path, os.R_OK):
        raise PermissionError(f"Insufficient permissions to read model file: {model_path}")
    
    # Load model using torch.load with secure defaults
    model = torch.load(model_path, map_location=torch.device('cpu'))
    if not isinstance(model, nn.Module):
        raise TypeError("Loaded object is not a PyTorch module")
    return model

def make_inference(model: nn.Module, input_data: torch.Tensor) -> torch.Tensor:
    """
    Perform secure inference on the given model.
    """
    if not isinstance(model, nn.Module):
        raise TypeError("Input model is not a PyTorch module")
    
    if not isinstance(input_data, torch.Tensor):
        raise TypeError("Input data must be a PyTorch tensor")
    
    # Ensure input tensor is on CPU
    if input_data.device.type != 'cpu':
        raise ValueError("Input data must be on CPU")
    
    # Perform inference
    with torch.no_grad():
        output = model(input_data)
    
    return output

def main():
    # Example usage
    model_path = "path/to/secure_model.pt"
    model = load_model(model_path)
    
    # Generate dummy input (replace with actual data)
    dummy_input = torch.randn(1, 1, 28, 28)
    
    output = make_inference(model, dummy_input)
    print("Inference result:", output)

if __name__ == "__main__":
    main()