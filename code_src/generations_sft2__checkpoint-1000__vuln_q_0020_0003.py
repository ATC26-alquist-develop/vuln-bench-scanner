import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms
import io
import os

def secure_predict(image_path: str, model_name: str = 'resnet50') -> dict:
    """
    Securely load a pre-trained PyTorch model and make a prediction on an image.
    
    Args:
        image_path: Path to the image file
        model_name: Name of the pre-trained model to use (default: 'resnet50')
    
    Returns:
        dict: Prediction results
    """
    # Validate inputs
    if not isinstance(image_path, str) or not isinstance(model_name, str):
        raise ValueError("Invalid input types")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    if not os.path.isfile(image_path):
        raise ValueError("Path must point to a file")
    
    # Load pre-trained model securely
    try:
        model = getattr(models, model_name)(pretrained=True)
        model.eval()  # Set model to evaluation mode
    except AttributeError:
        raise ValueError(f"Model {model_name} not found in torchvision.models")
    
    # Load and preprocess image securely
    try:
        with Image.open(image_path) as img:
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            input_tensor = preprocess(img)
            input_batch = input_tensor.unsqueeze(0)  # Add batch dimension
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")
    
    # Make prediction securely
    try:
        with torch.no_grad():  # Disable gradient calculation for inference
            output = model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            topk = probabilities.topk(5)  # Get top 5 predictions
            return {
                'predictions': topk.indices.tolist(),
                'probabilities': topk.values.tolist()
            }
    except Exception as e:
        raise RuntimeError(f"Error during prediction: {str(e)}")