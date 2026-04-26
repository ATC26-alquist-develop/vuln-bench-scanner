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
    Securely load a pre-trained PyTorch model with validated weights.
    
    Args:
        model_name: Name of the model architecture
        weights_path: Path to the model weights file
    
    Returns:
        Loaded PyTorch model
    
    Raises:
        ValueError: If model name or weights path is invalid
        RuntimeError: If model loading fails
    """
    # Validate model name
    valid_models = {
        'resnet18': models.resnet18,
        'resnet50': models.resnet50,
        'mobilenet_v2': models.mobilenet_v2
    }
    
    if model_name not in valid_models:
        raise ValueError(f"Unsupported model: {model_name}")
    
    model = valid_models[model_name]
    
    # Validate weights path
    if not os.path.exists(weights_path):
        raise ValueError(f"Invalid weights path: {weights_path}")
    
    # Load model with strict checking
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    model.eval()  # Set model to evaluation mode
    
    return model

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Securely preprocess an image for model prediction.
    
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
    Securely predict class probabilities for an image.
    
    Args:
        model: Pre-trained PyTorch model
        image_path: Path to the image file
    
    Returns:
        Tuple of (class probabilities, class names)
    """
    # Validate input
    if not isinstance(model, nn.Module):
        raise ValueError("Invalid model type")
    
    if not os.path.exists(image_path):
        raise ValueError(f"Invalid image path: {image_path}")
    
    # Load and preprocess image
    try:
        with Image.open(image_path) as img:
            processed = preprocess_image(img)
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")
    
    # Make prediction
    with torch.no_grad():
        outputs = model(processed)
        probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()[0]
    
    # Get top 5 predictions
    top5_indices = torch.argsort(probabilities)[-5:].tolist()
    top5_classes = [model.class_to_idx[str(i)] for i in top5_indices]
    top5_probs = probabilities[top5_indices]
    
    return top5_probs, top5_classes

# Example usage
if __name__ == "__main__":
    try:
        # Load pre-trained model (example with ResNet18)
        model = load_pretrained_model('resnet18', 'path/to/resnet18-f37072fd.pth')
        
        # Predict image
        probs, classes = predict_image(model, 'path/to/image.jpg')
        
        print(f"Top 5 probabilities: {probs}")