import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms
import os

def secure_predict(image_path: str, model_name: str = 'resnet50') -> dict:
    """
    Securely load a pre-trained PyTorch model and perform prediction on an image.
    
    Args:
        image_path: Path to the image file
        model_name: Name of the pre-trained model to use (default: 'resnet50')
    
    Returns:
        dict: Prediction results with class name and probability
    
    Raises:
        ValueError: If inputs are invalid
        FileNotFoundError: If image file doesn't exist
        RuntimeError: If model loading fails
    """
    # Validate inputs
    if not isinstance(image_path, str) or not isinstance(model_name, str):
        raise ValueError("Both image_path and model_name must be strings")
        
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    if not os.path.isfile(f"models/{model_name}.pth"):
        raise RuntimeError(f"Model file not found: models/{model_name}.pth")
        
    # Load pre-trained model securely
    try:
        model = models.__dict__[model_name](pretrained=True)
        model.eval()
    except KeyError:
        raise ValueError(f"Model {model_name} not found in torchvision.models")
        
    # Load model weights
    try:
        state_dict = torch.load(f"models/{model_name}.pth", map_location=torch.device('cpu'))
        model.load_state_dict(state_dict)
    except Exception as e:
        raise RuntimeError(f"Failed to load model weights: {str(e)}")
        
    # Define secure image preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # Load and preprocess image securely
    try:
        with Image.open(image_path) as img:
            img_tensor = preprocess(img).unsqueeze(0)
    except Exception as e:
        raise RuntimeError(f"Failed to process image: {str(e)}")
        
    # Perform prediction
    try:
        with torch.no_grad():
            outputs = model(img_tensor)
            _, predicted_idx = torch.max(outputs, 1)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            
            # Map index to class name (example for resnet50)
            class_names = ['class1', 'class2', 'class3', 'class4', 'class5']
            predicted_class = class_names[predicted_idx.item()]
            
            return {
                'class_name': predicted_class,
                'probability': float(probabilities[predicted_idx].item())
            }
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")