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
        ValueError: If invalid model or weights specified
        RuntimeError: If model loading fails
    """
    # Validate model name
    valid_models = {
        'resnet18': models.resnet18,
        'resnet50': models.resnet50,
        'mobilenet_v2': models.mobilenet_v2
    }
    
    if model_name not in valid_models:
        raise ValueError(f"Unsupported model. Must be one of: {list(valid_models.keys())}")
    
    model = valid_models[model_name]
    
    # Load pre-trained weights securely
    try:
        model.load_state_dict(torch.load(weights))
        model.eval()  # Set model to evaluation mode
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
        
    Raises:
        ValueError: If image is invalid
    """
    # Define secure preprocessing transforms
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225]),
    ])
    
    try:
        # Convert to tensor and add batch dimension
        tensor = preprocess(image).unsqueeze(0)
        return tensor
    except Exception as e:
        raise ValueError(f"Invalid image: {str(e)}")

def predict_image(model: nn.Module, image_path: str) -> dict:
    """
    Securely predict class probabilities for an image.
    
    Args:
        model: Pre-trained PyTorch model
        image_path: Path to input image
        
    Returns:
        Dictionary with class probabilities
        
    Raises:
        FileNotFoundError: If image file not found
        RuntimeError: If prediction fails
    """
    # Validate input
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Load and preprocess image
    try:
        with Image.open(image_path) as img:
            tensor = preprocess_image(img)
    except Exception as e:
        raise ValueError(f"Image processing error: {str(e)}")
    
    # Make prediction
    try:
        with torch.no_grad():
            outputs = model(tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            return probabilities.tolist()
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Load pre-trained model (example with ResNet18)
        model = load_pretrained_model('resnet18', 'https://download.pytorch.org/models/resnet18-f37072fd.pth')
        
        # Predict image
        result = predict_image(model, 'path/to/image.jpg')
        print("Predictions:", result)
        
    except Exception as e:
        print(f"Error: {str(e)}")