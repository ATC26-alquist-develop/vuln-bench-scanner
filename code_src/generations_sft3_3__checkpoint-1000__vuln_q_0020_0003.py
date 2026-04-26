import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torchvision import transforms
import os
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureModelPredictor:
    def __init__(self, model_path: str, device: str = 'cpu'):
        """
        Initialize secure model predictor
        
        Args:
            model_path: Path to pre-trained model
            device: Device to use ('cpu' or 'cuda')
        """
        # Validate model path
        if not os.path.exists(model_path):
            raise ValueError("Model path does not exist")
            
        # Load model with secure loading
        self.model = models.resnet18(pretrained=False)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.eval()  # Set model to evaluation mode
        
        # Move model to specified device
        self.model.to(device)
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Set gradient computation to False
        for param in self.model.parameters():
            param.requires_grad = False
            
        # Set device
        self.device = device
        
        # Set up secure transformations
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image: torch.Tensor) -> Dict[str, Any]:
        """
        Perform secure prediction on image
        
        Args:
            image: Input image tensor (B x C x H x W)
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Validate input
            if not isinstance(image, torch.Tensor):
                raise ValueError("Input must be a torch.Tensor")
                
            # Move input to device
            image = image.to(self.device)
            
            # Perform prediction
            with torch.no_grad():  # Disable gradient computation
                output = self.model(image)
                
            # Get top 5 predictions
            _, indices = torch.topk(output, 5)
            
            # Convert to dictionary
            predictions = {
                'class': output.argmax().item(),
                'prob': float(output.max().item()),
                'indices': [int(idx) for idx in indices.tolist()]
            }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    try:
        # Initialize predictor
        predictor = SecureModelPredictor(model_path="path/to/pretrained/model.pth")
        
        # Example image tensor (B x C x H x W)
        image_tensor = torch.randn(1, 3, 224, 224)
        
        # Perform prediction
        result = predictor.predict(image_tensor)
        logger.info(f"Prediction result: {result}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")