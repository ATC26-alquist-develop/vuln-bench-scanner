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
            
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Check for excessive file count
        self.max_files = max_files
        self.file_count = 0
        
        # Load images with security checks
        self.images = []
        for filename in os.listdir(self.root_dir):
            if self.file_count >= self.max_files:
                raise ValueError("Maximum file limit reached")
                
            file_path = os.path.join(self.root_dir, filename)
            if not os.path.isfile(file_path):
                continue
                
            try:
                # Verify file is an image
                img = Image.open(file_path)
                img.verify()
                
                # Calculate secure hash
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                self.images.append({
                    'path': file_path,
                    'hash': file_hash,
                    'size': img.size
                })
                self.file_count += 1
                
            except Exception as e:
                self.logger.warning(f"Skipping invalid file: {filename}")
                continue
                
        # Set transform if provided
        self.transform = transform
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        if idx >= len(self.images):
            raise IndexError("Index out of range")
            
        item = self.images[idx]
        
        # Apply transform if provided
        if self.transform:
            item['image'] = self.transform(Image.open(item['path']))
            
        return item

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader
    
    Args:
        dataset: SecureImageDataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of worker processes for DataLoader
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
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True
    )