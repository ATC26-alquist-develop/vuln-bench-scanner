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
            transform: Optional image transformation
        """
        super().__init__()
        
        # Validate inputs
        if not isinstance(image_paths, list) or not all(isinstance(p, str) for p in image_paths):
            raise ValueError("image_paths must be a list of strings")
            
        # Validate paths
        self.image_paths = []
        self.image_hashes = []
        self.transform = transform
        
        # Validate and limit number of images
        for path in image_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image path not found: {path}")
                
            # Verify file is actually an image
            try:
                with Image.open(path) as img:
                    img.verify()
            except Exception as e:
                raise ValueError(f"Invalid image file: {path}")
                
            # Calculate secure hash of file
            with open(path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                self.image_hashes.append(file_hash)
                
            self.image_paths.append(path)
            
        self.image_paths = self.image_paths[:max_size]
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        if idx >= len(self.image_paths):
            raise IndexError("Index out of range")
            
        path = self.image_paths[idx]
        
        # Read and preprocess image
        try:
            img = Image.open(path)
            img = img.convert('RGB')  # Ensure RGB format
            
            if self.transform:
                img = self.transform(img)
                
            return img, torch.tensor(self.image_hashes[idx], dtype=torch.int64)
            
        except Exception as e:
            raise ValueError(f"Error processing image: {path}")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    shuffle: bool = True,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader with proper validation
    
    Args:
        dataset: Validated dataset instance
        batch_size: Batch size
        shuffle: Whether to shuffle the data
        num_workers: Number of worker processes for data loading
        
    Returns:
        DataLoader instance
    """
    if not isinstance(dataset, SecureImageDataset):
        raise ValueError("Invalid dataset type")
        
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Invalid batch size")
        
    if not isinstance(num_workers, int) or num_workers < 0:
        raise ValueError("Invalid number of workers")
        
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True,
        collate_fn=collate_fn  # Custom collate function
    )

def collate_fn(batch):
    """
    Custom collate function to handle mixed types
    """
    images, targets = zip(*batch)
    return torch.stack(images), torch.cat(targets)