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
        'resnet18': models.resnet18,
        'resnet50': models.resnet50,
        'mobilenet_v2': models.mobilenet_v2
    }
    
    if model_name not in valid_models:
        raise ValueError(f"Unsupported model: {model_name}")
    
    model_class = valid_models[model_name]
    
    # Load model with strict type checking
    model = model_class(weights=models.MobileNet_V2_Weights.DEFAULT)
    
    # Validate weights path
    if not os.path.exists(weights_path):
        raise ValueError(f"Invalid weights path: {weights_path}")
    
    # Load weights with strict type checking
    try:
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    except Exception as e:
        raise RuntimeError(f"Failed to load model weights: {str(e)}")
    
    return model.eval()

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Securely preprocess an image for model inference
    
    Args:
        image: PIL Image object
    
    Returns:
        Preprocessed tensor
    """
    # Define secure preprocessing transforms
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225]),
    ])
    
    # Convert to tensor and apply preprocessing
    tensor = preprocess(image)
    return tensor.unsqueeze(0)  # Add batch dimension

def predict_image(model: nn.Module, image_path: str) -> tuple:
    """
    Perform secure image prediction
    
    Args:
        model: Pre-trained model
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
        raise ValueError(f"Failed to process image: {str(e)}")
    
    # Perform prediction
    try:
        with torch.no_grad():
            output = model(processed)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            top_prob, top_class = probabilities.topk(1, dim=1)
        return top_class.item(), float(top_prob.item())
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Load pre-trained model (example with ResNet18)
        model = load_pretrained_model('resnet18', 'path/to/weights.pth')
        
        # Predict image
        image_path = 'path/to/image.jpg'
        prediction, probability = predict_image(model, image_path)
        
        print(f"Predicted class: {prediction}")
        print(f"Probability: {probability:.