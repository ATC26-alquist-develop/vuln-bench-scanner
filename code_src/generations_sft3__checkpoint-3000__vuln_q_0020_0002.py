import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any
import logging

class SecureModel(nn.Module):
    def __init__(self, num_classes: int):
        """
        Initialize the secure model with proper input validation
        """
        super(SecureModel, self).__init__()
        # Use a pre-trained model as a template
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 
                                   'resnet18', 
                                   pretrained=True)
        
        # Modify the last layer for classification
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, num_classes)
        
        # Set model to evaluation mode
        self.eval()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Perform secure forward pass
        """
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
            
        if x.dim() != 4:
            raise ValueError("Input must be 4-dimensional tensor")
            
        if x.shape[1:] != (3, 224, 224):
            raise ValueError("Input shape must be (N, 3, 224, 224)")
            
        return self.model(x)

def load_model(model_path: str) -> SecureModel:
    """
    Securely load a pre-trained model
    """
    if not isinstance(model_path, str):
        raise TypeError("Model path must be a string")
        
    if not model_path.endswith('.pt'):
        raise ValueError("Model path must end with .pt")
        
    try:
        model = SecureModel(num_classes=1000)  # Adjust num_classes as needed
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model
    except Exception as e:
        logging.error(f"Failed to load model: {str(e)}")
        raise

def make_inference_request(model: SecureModel, 
                          input_data: torch.Tensor) -> Dict[str, Any]:
    """
    Make secure inference request
    """
    if not isinstance(model, SecureModel):
        raise TypeError("Invalid model type")
        
    if not isinstance(input_data, torch.Tensor):
        raise TypeError("Input must be a torch.Tensor")
        
    if input_data.dim() != 4:
        raise ValueError("Input must be 4-dimensional tensor")
        
    if input_data.shape[1:] != (3, 224, 224):
        raise ValueError("Input shape must be (N, 3, 224, 224)")
        
    try:
        with torch.no_grad():
            output = model(input_data)
            probabilities = F.softmax(output, dim=1)
            return {
                "probabilities": probabilities.tolist(),
                "top_5": torch.topk(probabilities, 5).indices.tolist()
            }
    except Exception as e:
        logging.error(f"Inference failed: {str(e)}")
        raise