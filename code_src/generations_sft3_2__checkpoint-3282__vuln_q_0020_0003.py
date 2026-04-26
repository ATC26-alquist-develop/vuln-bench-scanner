```python
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import io
import os

def load_pretrained_model(model_name: str, weights: str) -> nn.Module:
    """
    Securely load a pre-trained PyTorch model with specified weights.
    
    Args:
        model_name: Name of the model architecture
        weights: Pre-trained weights to load
        
    Returns:
        Loaded model
    
    Raises:
        ValueError: If model or weights are invalid
        RuntimeError: If model loading fails
    """
    # Validate model name
    valid_models = {
        'resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152',
        'vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn',
        'vgg19_bn'
    }
    if model_name not in valid_models:
        raise ValueError(f"Unsupported model architecture: {model_name}")
    
    # Validate weights
    valid_weights = {
        'IMAGENET1K_V1', 'IMAGENET1K_V2'
    }
    if weights not in valid_weights:
        raise ValueError(f"Unsupported weights: {weights}")
    
    # Load model with specific weights
    try:
        model = getattr(models, model_name)(weights=weights)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Securely preprocess an image for model inference.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed tensor
    """
    # Define preprocessing transforms
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225]),
    ])
    
    try:
        # Convert to tensor and apply preprocessing
        tensor = preprocess(image)
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        return tensor
    except Exception as e:
        raise RuntimeError(f"Image preprocessing failed: {str(e)}")

def make_prediction(model: nn.Module, image_path: str) -> tuple:
    """
    Make a prediction using a pre-trained model.
    
    Args:
        model: Pre-trained PyTorch model
        image_path: Path to input image
        
    Returns:
        Tuple of (model output, class probabilities)
    """
    # Validate input
    if not isinstance(model, nn.Module):
        raise ValueError("Invalid model")
    if not isinstance(image_path, str):
        raise ValueError("Invalid image path")
        
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    # Load and preprocess image
    try:
        with Image.open(image_path) as img:
            tensor = preprocess_image(img)
    except Exception as e:
        raise RuntimeError(f"Image loading failed: {str(e)}")
    
    # Make prediction
    try:
        with torch.no_grad():
            output = model(tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
    except Exception as e:
        raise RuntimeError(f"Model prediction failed: {str(e)}")
    
    return output, probabilities

# Example usage
if __name__ == "__main__":
    try:
        # Load pre-trained model
        model = load_pretrained_model