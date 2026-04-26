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
        """
        # Validate model path
        if not os.path.exists(model_path):
            raise ValueError("Model file does not exist")
            
        # Load model with strict parameters
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(pretrained=False)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()  # Set model to evaluation mode
        
        # Define secure transformations
        self.transform = transforms.Compose([
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
        if image.format not in ['JPEG', 'PNG']:
            return False
        if image.size[0] > 2048 or image.size[1] > 2048:
            return False
        return True

    def predict(self, image_path: str) -> dict:
        """
        Securely predict image class
        """
        try:
            # Validate input path
            if not os.path.exists(image_path):
                raise ValueError("Image file does not exist")
                
            # Validate image
            with open(image_path, 'rb') as f:
                image = Image.open(io.BytesIO(f.read()))
                if not self._validate_image(image):
                    raise ValueError("Invalid image format or size")
                
            # Convert to tensor
            img_tensor = self.transform(image)
            img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
            
            # Make prediction
            with torch.no_grad():
                output = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(output, dim=1)
                
            # Get top 5 predictions
            top5_probs, top5_labels = torch.topk(probabilities, 5)
            
            # Return results
            return {
                'class': top5_labels[0].item(),
                'probabilities': top5_probs.tolist()
            }
            
        except Exception as e:
            # Log error securely (implement proper logging)
            raise RuntimeError("Prediction failed") from e