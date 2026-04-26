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
        
        # Set secure random number generator
        torch.manual_seed(42)
        
    def preprocess_image(self, image: Any) -> torch.Tensor:
        """
        Preprocess image securely
        
        Args:
            image: Image to preprocess
            
        Returns:
            Preprocessed tensor
        """
        # Validate input type
        if not isinstance(image, (torch.Tensor, str, bytes)):
            raise ValueError("Invalid input type")
            
        # Convert to tensor if bytes or string
        if isinstance(image, (bytes, str)):
            image = transforms.ToTensor()(image)
            
        # Validate tensor dimensions
        if image.dim() != 3 or image.size(0) != 3:
            raise ValueError("Invalid image dimensions")
            
        # Normalize image
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])
        
        return transform(image)
    
    def predict(self, image: Any) -> Dict[str, Any]:
        """
        Perform secure prediction
        
        Args:
            image: Image to predict
            
        Returns:
            Prediction result
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Add batch dimension
            processed_image = processed_image.unsqueeze(0)
            
            # Move to device
            processed_image = processed_image.to(self.model.device)
            
            # Perform prediction
            with torch.no_grad():
                output = self.model(processed_image)
                
            # Get top 5 predictions
            _, indices = torch.topk(output, 5)
            
            # Convert to list of tuples
            predictions = [(self.model.classifier[1].weight[i].tolist(),
                           self.model.classifier[1].bias[i].item())
                           for i in indices[0].tolist()]
            
            return {
                "predictions": predictions,
                "model_name": "resnet18",
                "version": "1.0.0"
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise