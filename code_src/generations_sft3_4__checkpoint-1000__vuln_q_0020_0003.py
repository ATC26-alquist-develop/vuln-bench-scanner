import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torchvision import transforms
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureModelPredictor:
    def __init__(self, model_path: str, max_batch_size: int = 1):
        """
        Initialize secure model predictor with strict validation
        
        Args:
            model_path: Path to pre-trained model
            max_batch_size: Maximum batch size for predictions
        """
        # Validate inputs
        if not isinstance(model_path, str):
            raise ValueError("Model path must be a string")
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model file not found")
        if not isinstance(max_batch_size, int) or max_batch_size <= 0:
            raise ValueError("max_batch_size must be a positive integer")
            
        self.max_batch_size = max_batch_size
        
        # Load model with strict validation
        self.model = self._load_model(model_path)
        self.model.eval()  # Set model to evaluation mode
        
        # Set up secure transformations
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])

    def _load_model(self, model_path: str) -> nn.Module:
        """
        Securely load pre-trained model
        
        Args:
            model_path: Path to pre-trained model
        
        Returns:
            Loaded PyTorch model
        """
        try:
            # Load model with strict validation
            model = models.resnet18(pretrained=True)
            model.load_state_dict(torch.load(model_path, map_location='cpu'))
            model.eval()  # Ensure model is in evaluation mode
            
            # Validate model structure
            if not isinstance(model, nn.Module):
                raise ValueError("Invalid model structure")
                
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def predict(self, image: torch.Tensor) -> Optional[torch.Tensor]:
        """
        Perform secure prediction on a single image
        
        Args:
            image: Input image tensor (B x C x H x W)
        
        Returns:
            Predicted probabilities or None if validation fails
        """
        try:
            # Validate input
            if not isinstance(image, torch.Tensor):
                raise ValueError("Input must be a PyTorch tensor")
            if image.dim() != 4:
                raise ValueError("Invalid input dimensions")
                
            # Validate batch size
            if image.shape[0] > self.max_batch_size:
                raise ValueError(f"Batch size exceeds maximum allowed: {self.max_batch_size}")
                
            # Perform prediction
            with torch.no_grad():
                output = self.model(image)
                
            return output
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return None