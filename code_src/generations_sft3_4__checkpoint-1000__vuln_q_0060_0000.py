import os
import torch
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import hashlib
import logging
from typing import List, Optional

class SecureImageDataset(Dataset):
    """Secure implementation of a custom image dataset"""
    
    def __init__(
        self,
        root_dir: str,
        transform: Optional[transforms.Compose] = None,
        max_files: int = 1000000
    ):
        """
        Initialize the dataset with security measures
        
        Args:
            root_dir: Root directory containing images
            transform: Optional transform to apply to images
            max_files: Maximum number of files to load (prevents DoS)
        """
        super().__init__()
        
        # Validate and sanitize input paths
        self.root_dir = os.path.abspath(root_dir)
        if not os.path.exists(self.root_dir):
            raise ValueError("Root directory does not exist")
            
        # Set up secure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate and limit number of files
        self.max_files = max_files
        self.file_list = []
        for root, _, files in os.walk(self.root_dir):
            self.file_list.extend([os.path.join(root, f) for f in files])
            if len(self.file_list) >= self.max_files:
                break
                
        # Validate all files are images
        self.image_files = []
        for file_path in self.file_list:
            try:
                with Image.open(file_path) as img:
                    self.image_files.append(file_path)
            except Exception as e:
                self.logger.warning(f"Invalid image file: {file_path}")
                continue
                
        # Validate all files are within root directory
        for file_path in self.image_files:
            if not os.path.abspath(file_path).startswith(self.root_dir):
                raise ValueError("Invalid file path detected")
                
        # Set up transform if provided
        self.transform = transform
        
    def __len__(self):
        """Return number of images in dataset"""
        return len(self.image_files)
    
    def __getitem__(self, idx):
        """Get image at index with security measures"""
        if idx >= len(self):
            raise IndexError("Index out of range")
            
        file_path = self.image_files[idx]
        
        # Validate file still exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
            
        try:
            with Image.open(file_path) as img:
                # Apply transform if provided
                if self.transform:
                    img = self.transform(img)
                return img
        except Exception as e:
            self.logger.error(f"Error processing image {file_path}: {str(e)}")
            raise ValueError(f"Invalid image file: {file_path}")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader with proper validation
    
    Args:
        dataset: SecureImageDataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of workers for DataLoader
    """
    # Validate inputs
    if not isinstance(dataset, SecureImageDataset):
        raise TypeError("Invalid dataset type")
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