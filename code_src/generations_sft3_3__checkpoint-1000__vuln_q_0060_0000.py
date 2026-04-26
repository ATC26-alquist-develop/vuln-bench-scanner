```python
import os
import torch
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import logging
from typing import List, Optional
import hashlib

class SecureImageDataset(Dataset):
    """Secure implementation of a custom image dataset"""
    
    def __init__(
        self,
        image_paths: List[str],
        transform: Optional[transforms.Compose] = None,
        max_size: int = 1000000
    ):
        """
        Initialize the dataset with security measures
        
        Args:
            image_paths: List of image file paths
            transform: Optional image transformation
            max_size: Maximum number of images to load
        """
        # Validate input
        if not isinstance(image_paths, list) or not all(isinstance(p, str) for p in image_paths):
            raise ValueError("image_paths must be a list of strings")
        
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError("max_size must be a positive integer")
            
        # Validate paths
        self.image_paths = []
        for path in image_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image path not found: {path}")
            if not os.path.isfile(path):
                raise ValueError(f"Path is not a file: {path}")
            self.image_paths.append(path)
            
        # Validate max_size
        if len(self.image_paths) > max_size:
            raise ValueError(f"Too many images: {len(self.image_paths)} > {max_size}")
            
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Set transform if provided
        self.transform = transform
        
        # Calculate hash for integrity check
        self.image_hash = hashlib.sha256()
        for path in self.image_paths:
            with open(path, 'rb') as f:
                self.image_hash.update(f.read())
        
    def __len__(self):
        """Return number of images"""
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        """Get item with security measures"""
        if idx < 0 or idx >= len(self):
            raise IndexError("Index out of range")
            
        # Validate path
        if not os.path.exists(self.image_paths[idx]):
            raise FileNotFoundError(f"Image path not found: {self.image_paths[idx]}")
            
        # Read image with size limit
        max_size = 1024 * 1024 * 10  # 10MB limit
        try:
            with open(self.image_paths[idx], 'rb') as f:
                if len(f.read()) > max_size:
                    raise ValueError("Image file too large")
                img = Image.open(f)
        except Exception as e:
            self.logger.error(f"Error reading image {self.image_paths[idx]}: {str(e)}")
            raise ValueError(f"Error processing image: {str(e)}")
            
        # Apply transform if provided
        if self.transform:
            img = self.transform(img)
            
        # Calculate hash for integrity check
        with open(self.image_paths[idx], 'rb') as f:
            img_hash = hashlib.sha256(f.read()).hexdigest()
            
        # Verify integrity
        if img_hash != self.image_hash.hexdigest():
            self.logger.error(f"Integrity check failed for image {self.image_paths[idx]}")
            raise ValueError("Image integrity check failed")
            
        return img

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure dataloader
    
    Args:
        dataset: SecureImageDataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of worker