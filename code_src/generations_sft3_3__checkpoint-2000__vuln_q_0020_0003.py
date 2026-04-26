import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os
from typing import Tuple, Optional

class SecureImageClassifier:
    def __init__(self, model_path: str, max_image_size: int = 256):
        """
        Initialize secure image classifier with pre-trained model
        
        Args:
            model_path: Path to pre-trained PyTorch model
            max_image_size: Maximum allowed image size
        """
        # Verify model path exists and is a file
        if not os.path.isfile(model_path):
            raise ValueError("Model path must be a valid file")
            
        # Load pre-trained model (e.g. ResNet18)
        self.model = models.resnet18(pretrained=True)
        self.model.eval()  # Set model to evaluation mode
        
        # Load model state dictionary
        checkpoint = torch.load(model_path, map_location='cpu')
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Set secure image processing transforms
        self.transform = transforms.Compose([
            transforms.Resize(min(max_image_size, 256)),  # Limit max size
            transforms.CenterCrop(224),  # ResNet18 input size
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])

    def _validate_image(self, image: Image.Image) -> bool:
        """
        Validate image meets security requirements
        
        Args:
            image: PIL Image object
            
        Returns:
            bool: True if image is valid, False otherwise
        """
        # Check image size
        if image.width > 1000 or image.height > 1000:
            return False
            
        # Check image format
        if image.format not in ['JPEG', 'PNG']:
            return False
            
        return True

    def predict(self, image_path: str) -> Optional[Tuple[str, float]]:
        """
        Perform secure image classification
        
        Args:
            image_path: Path to input image
            
        Returns:
            Optional[Tuple[str, float]]: Tuple of (class label, confidence)
            or None if validation fails
        """
        try:
            # Validate input path
            if not os.path.isfile(image_path):
                return None
                
            # Load and validate image
            with Image.open(image_path) as img:
                if not self._validate_image(img):
                    return None
                    
                # Convert to tensor and normalize
                img_tensor = self.transform(img)
                img_batch = img_tensor.unsqueeze(0)  # Add batch dimension
                
            # Perform inference
            with torch.no_grad():
                output = self.model(img_batch)
                probabilities = torch.nn.functional.softmax(output, dim=1)
                
            # Get top class and confidence
            _, predicted_class = torch.max(probabilities, 1)
            class_label = self.model.class_to_idx
            confidence = float(probabilities[0][predicted_class].item())
            
            return (list(class_label.keys())[list(class_label.values()).index(predicted_class.item())], 
                    confidence)
            
        except Exception as e:
            # Log error securely (implement proper logging)
            return None