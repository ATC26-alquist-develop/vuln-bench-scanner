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
            
        # Load model with secure parameters
        self.model = models.resnet18(pretrained=False)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()  # Set model to evaluation mode
        
        # Move model to specified device
        self.model.to(device)
        
        # Set secure parameters
        self.device = device
        self.model = self.model.to(device)
        
    def _validate_input(self, image: Any) -> bool:
        """
        Validate input image
        """
        if not isinstance(image, (torch.Tensor, str)):
            logger.error("Invalid input type")
            return False
            
        if isinstance(image, str):
            # Validate image file
            if not os.path.exists(image):
                logger.error("Image file does not exist")
                return False
                
            # Validate image size
            try:
                img = transforms.functional.to_tensor(transforms.functional.open_image(image))
                if img.size(1) != 224 or img.size(2) != 224:
                    logger.error("Invalid image size")
                    return False
            except Exception as e:
                logger.error(f"Image validation error: {str(e)}")
                return False
                
        return True
    
    def predict(self, image: Any) -> Dict[str, Any]:
        """
        Perform secure prediction
        
        Args:
            image: Input image (tensor or path to image file)
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Validate input
            if not self._validate_input(image):
                raise ValueError("Invalid input")
            
            # Convert to tensor if needed
            if isinstance(image, str):
                image = transforms.functional.to_tensor(transforms.functional.open_image(image))
                
            # Move to device
            image = image.to(self.device)
            
            # Make prediction
            with torch.no_grad():
                output = self.model(image.unsqueeze(0))
                
            # Get top 5 predictions
            _, indices = torch.topk(output, 5)
            
            # Convert to dictionary
            result = {
                "class": output.argmax().item(),
                "prob": float(output.max().item()),
                "top5": [(str(self.model.classifier[1].weight[i].argmax()), float(output[i].item())) 
                         for i in indices[0].tolist()]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise