```python
import torch
import torchvision.models as models
from PIL import Image
import io
import requests
from typing import Optional, Tuple
import os

def secure_predict(image_path: str, model_name: str = 'resnet50') -> Optional[Tuple[str, float]]:
    """
    Securely load a pre-trained PyTorch model and make a prediction on an image.
    
    Args:
        image_path: Path to the image file
        model_name: Name of the pre-trained model to use (default: resnet50)
    
    Returns:
        Tuple of (predicted_class, confidence) or None if input is invalid
    """
    # Validate model name
    allowed_models = {'resnet50', 'vgg16', 'inceptionv3'}
    if model_name.lower() not in allowed_models:
        raise ValueError(f"Unsupported model. Allowed models: {allowed_models}")

    try:
        # Load pre-trained model securely
        model = models.__dict__[model_name](pretrained=True)
        model.eval()  # Set model to evaluation mode
        
        # Validate image file
        if not os.path.isfile(image_path) or not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError("Invalid image file path")
            
        # Load and preprocess image securely
        with Image.open(image_path) as img:
            img = img.convert('RGB')  # Convert to RGB to ensure consistency
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            input_tensor = preprocess(img)
            input_batch = input_tensor.unsqueeze(0)  # Add batch dimension
            
        # Make prediction securely
        with torch.no_grad():  # Disable gradient calculation for efficiency
            output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            topk_prob, topk_idx = probabilities.topk(1, sorted=True)
            predicted_class = topk_idx[0].item()
            confidence = topk_prob[0].item()
            
        return predicted_class, confidence
        
    except Exception as e:
        # Log error securely (implement proper logging mechanism)
        print(f"Error during prediction: {str(e)}")
        return None
```