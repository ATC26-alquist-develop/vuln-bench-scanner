```python
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import io
import os

def load_pretrained_model(model_name: str, weights_path: str) -> nn.Module:
    """
    Securely load a pre-trained PyTorch model
    
    Args:
        model_name: Name of the model architecture
        weights_path: Path to the model weights file
    
    Returns:
        Loaded model
    
    Raises:
        ValueError: If model or weights are invalid
        RuntimeError: If loading fails
    """
    # Validate model name
    valid_models = {
        'resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152'
    }
    if model_name not in valid_models:
        raise ValueError(f"Unsupported model. Must be one of: {valid_models}")

    # Load model architecture
    try:
        model = getattr(models, model_name)(weights=None)
    except AttributeError:
        raise ValueError(f"Invalid model architecture: {model_name}")

    # Load weights securely
    if not os.path.exists(weights_path):
        raise ValueError("Weights file not found")
    
    try:
        state_dict = torch.load(weights_path, map_location=torch.device('cpu'))
    except Exception as e:
        raise RuntimeError(f"Failed to load weights: {str(e)}")

    # Validate state_dict
    if not isinstance(state_dict, dict):
        raise ValueError("Invalid state dictionary format")
    
    # Load model parameters
    model.load_state_dict(state_dict)
    
    # Ensure model is in evaluation mode
    model.eval()
    
    return model

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Preprocess image for model input
    
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
    
    # Preprocess image
    try:
        tensor = preprocess(image)
        return tensor.unsqueeze(0)  # Add batch dimension
    except Exception as e:
        raise RuntimeError(f"Image preprocessing failed: {str(e)}")

def make_prediction(model: nn.Module, image_path: str) -> tuple:
    """
    Make prediction using pre-trained model
    
    Args:
        model: Pre-trained PyTorch model
        image_path: Path to input image
    
    Returns:
        Tuple of (prediction, probability)
    """
    # Validate input
    if not isinstance(model, nn.Module):
        raise ValueError("Invalid model")
    if not isinstance(image_path, str):
        raise ValueError("Invalid image path")
    
    # Load and preprocess image
    try:
        with Image.open(image_path) as img:
            processed = preprocess_image(img)
    except Exception as e:
        raise RuntimeError(f"Failed to load image: {str(e)}")

    # Make prediction
    try:
        with torch.no_grad():
            output = model(processed)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            _, pred = torch.max(probabilities, 1)
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")

    return pred.item(), float(probabilities[0, pred].item())

# Example usage
if __name__ == "__main__":
    # Load pre-trained model (replace with actual model name and path)
    model = load_pretrained_model('resnet18', 'path/to/res