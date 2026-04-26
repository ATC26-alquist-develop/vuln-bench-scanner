import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import io
import os
import hashlib

class SecureModelPredictor:
    def __init__(self, model_path: str, max_image_size: int = 2048):
        """
        Initialize secure model predictor with strict validation
        
        Args:
            model_path: Path to pre-trained model
            max_image_size: Maximum allowed image size
        """
        # Validate model path
        if not os.path.exists(model_path):
            raise ValueError("Model path does not exist")
            
        # Load model with strict parameters
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(pretrained=False)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        self.model.to(self.device)
        
        # Set strict input validation
        self.transforms = transforms.Compose([
            transforms.Resize(min(256, max_image_size)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])
        
    def _validate_image(self, image: Image.Image) -> bool:
        """
        Validate image before processing
        """
        if not isinstance(image, Image.Image):
            return False
            
        # Check image size
        if image.width > 2048 or image.height > 2048:
            return False
            
        # Verify image format
        if image.format not in ['JPEG', 'PNG']:
            return False
            
        return True
    
    def predict(self, image_path: str) -> dict:
        """
        Securely predict image class
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        if not isinstance(image_path, str):
            raise ValueError("Invalid input type")
            
        # Validate file exists
        if not os.path.exists(image_path):
            raise ValueError("Image file does not exist")
            
        # Validate file size
        if os.path.getsize(image_path) > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("Image file too large")
            
        try:
            # Load and validate image
            with Image.open(image_path) as img:
                if not self._validate_image(img):
                    raise ValueError("Invalid image format or size")
                    
                # Convert to tensor
                img_tensor = self.transforms(img)
                img_tensor = img_tensor.unsqueeze(0).to(self.device)
                
            # Make prediction
            with torch.no_grad():
                output = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(output, dim=1)
                
            # Get top 5 predictions
            top5_probs, top5_labels = torch.topk(probabilities, 5)
            
            # Return results
            return {
                "class": top5_labels[0].item(),
                "probabilities": [float(p) for p in top5_probs.tolist()]
            }
            
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")