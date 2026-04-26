```python
from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image
import torch
import torchvision.transforms as transforms
from typing import List, Tuple
import hashlib

class SecureImageDataset(Dataset):
    def __init__(
        self,
        image_dir: str,
        max_file_size: int = 100_000_000,  # 100MB limit per file
        transform: List[transforms.Compose] = None
    ):
        """
        Initialize secure image dataset with strict validation
        
        Args:
            image_dir: Directory containing images
            max_file_size: Maximum allowed file size in bytes
            transform: List of transforms to apply to images
        """
        super().__init__()
        
        # Validate and sanitize input
        if not isinstance(image_dir, str) or not image_dir:
            raise ValueError("Invalid image directory")
            
        self.image_dir = os.path.abspath(image_dir)
        self.max_file_size = max_file_size
        
        # Validate directory exists and is accessible
        if not os.path.isdir(self.image_dir):
            raise ValueError("Image directory does not exist")
            
        # Get image files with validation
        self.images = []
        for root, _, files in os.walk(self.image_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    # Validate file size
                    if os.path.getsize(file_path) > self.max_file_size:
                        raise ValueError("File exceeds maximum allowed size")
                        
                    # Validate file extension
                    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        continue
                        
                    # Validate file permissions
                    if not os.access(file_path, os.R_OK):
                        continue
                        
                    self.images.append(file_path)
                    
        # Initialize transforms if provided
        self.transform = transform
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        if idx >= len(self.images):
            raise IndexError("Index out of range")
            
        image_path = self.images[idx]
        
        # Validate file still exists
        if not os.path.isfile(image_path):
            raise ValueError("Image file no longer exists")
            
        try:
            # Open image with size limit
            with Image.open(image_path) as img:
                # Apply transforms if provided
                if self.transform:
                    img = img.convert('RGB')  # Ensure RGB format
                    img = self.transform[0](img)
                else:
                    img = transforms.ToTensor()(img)
                    
            return img, image_path  # Return tensor and original path
                
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4,
    pin_memory: bool = True
) -> DataLoader:
    """
    Create a secure DataLoader with proper validation
    
    Args:
        dataset: Validated dataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of worker processes for DataLoader
        pin_memory: Whether to pin memory for faster data transfer
        
    Returns:
        DataLoader instance
    """
    # Validate inputs
    if not isinstance(dataset, SecureImageDataset):
        raise ValueError("Invalid dataset type")
        
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Invalid batch size")
        
    if not isinstance(num_workers, int) or num_workers < 0:
        raise ValueError("Invalid number of workers")
        
    # Create DataLoader with proper validation
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,  # Shuffle for reproduc