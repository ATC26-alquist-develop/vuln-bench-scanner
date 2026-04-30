```python
import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_image_path(image_path: str) -> None:
    """Validate that the image file exists and is a valid image file."""
    if not os.path.isfile(image_path):
        raise ValueError(f"Image file not found: {image_path}")
    
    # Check file extension
    if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError(f"Unsupported file type. Please use .png or .jpg")

def preprocess_image(image_path: str) -> torch.Tensor:
    """Preprocess the image for model prediction."""
    try:
        # Validate image path
        validate_image_path(image_path)
        
        # Load image with size limit to prevent memory issues
        with Image.open(image_path) as img:
            # Convert to RGB to ensure consistent channel count
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize while maintaining aspect ratio
            max_size = (1024, 1024)  # Reasonable maximum size
            img.thumbnail((max_size[0], max_size[1]), Image.LANCZOS)
            
            # Convert to tensor and normalize
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            return transform(img)
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise

def predict_image(model_path: str, image_path: str) -> Optional[str]:
    """
    Perform prediction using a pre-trained PyTorch model.
    
    Args:
        model_path: Path to the pre-trained model
        image_path: Path to the image file
        
    Returns:
        Predicted class label or None if prediction fails
    """
    try:
        # Validate model path
        if not os.path.isfile(model_path):
            raise ValueError(f"Model file not found: {model_path}")

        # Load model and set to evaluation mode
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = torch.load(model_path, map_location=device)
        model.eval()

        # Validate and preprocess image
        with torch.no_grad():  # Disable gradient calculation for inference
            try:
                image_tensor = preprocess_image(image_path)
                image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension
            except Exception as e:
                logging.error(f"Error preprocessing image: {str(e)}")
                return None

            # Move tensor to device
            image_tensor = image_tensor.to(device)

            # Perform prediction
            try:
                with torch.cuda.amp.autocast():  # Enable mixed precision
                    outputs = model(image_tensor)
                    _, predicted_idx = torch.max(outputs, 1)
                
                # Convert index to label (implement your own mapping)
                # For demonstration, we'll just return the index
                return str(predicted_idx.item())
            except Exception as e:
                logging.error(f"Error during prediction: {str(e)}")
                return None

    except Exception as e:
        logging.error(f"Error in prediction process: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    model_path = "path/to/pretrained/model.pth"
    image_path = "path/to/image.jpg"
    
    try:
        result = predict_image(model_path, image_path)
        if result:
            logging.info(f"Prediction result: {result}")
        else: