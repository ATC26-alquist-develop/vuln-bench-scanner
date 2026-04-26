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
        image_paths: List[str],
        max_size: int = 1000,
        transform: transforms.Compose = None
    ):
        """
        Secure implementation of a custom image dataset
        
        Args:
            image_paths: List of image file paths
            max_size: Maximum number of images to load
            transform: Optional image transformations
        """
        super().__init__()
        
        # Validate inputs
        if not isinstance(image_paths, list) or not all(isinstance(p, str) for p in image_paths):
            raise ValueError("image_paths must be a list of strings")
            
        # Validate paths
        self.image_paths = []
        self.image_hashes = []
        self.transform = transform if transform else transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])
        
        # Validate paths and load images securely
        for path in image_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image path not found: {path}")
                
            # Verify file is an image
            try:
                with Image.open(path) as img:
                    img.verify()
            except Exception as e:
                raise ValueError(f"Invalid image file: {path}")
                
            # Calculate secure hash
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                
            self.image_paths.append(path)
            self.image_hashes.append(file_hash)
            
        # Enforce size limit
        if len(self.image_paths) > max_size:
            raise ValueError(f"Too many images. Maximum allowed: {max_size}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Secure access to image
        path = self.image_paths[idx]
        hash_value = self.image_hashes[idx]
        
        try:
            image = Image.open(path)
            image = self.transform(image)
            return image, hash_value
        except Exception as e:
            raise ValueError(f"Error processing image: {path}")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader
    
    Args:
        dataset: SecureImageDataset instance
        batch_size: Batch size
        num_workers: Number of data loading workers
        
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
        
    # Create DataLoader with security measures
    return DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=True,
        pin_memory=True,
        drop_last=True
    )