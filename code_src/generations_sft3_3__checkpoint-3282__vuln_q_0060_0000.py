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
        root_dir: str,
        image_extensions: List[str] = ['.jpg', '.jpeg', '.png'],
        max_file_size: int = 1024 * 1024 * 1024,  # 1GB limit
        transform: transforms.Compose = None
    ):
        """
        Secure implementation of a custom image dataset
        
        Args:
            root_dir: Root directory containing images
            image_extensions: Allowed image file extensions
            max_file_size: Maximum allowed file size in bytes
            transform: Optional image transformations
        """
        super().__init__()
        
        # Validate and sanitize input paths
        if not os.path.isdir(root_dir):
            raise ValueError("Invalid root directory")
            
        self.root_dir = os.path.abspath(root_dir)
        
        # Validate and sanitize image extensions
        self.image_extensions = [ext.lower() for ext in image_extensions 
                                if ext.startswith('.')]
        
        # Validate transform parameters
        if transform is not None and not isinstance(transform, transforms.Compose):
            raise ValueError("Invalid transform parameter")
            
        self.transform = transform
        
        # Scan directory for images
        self.image_paths = []
        for dirpath, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in self.image_extensions):
                    file_path = os.path.join(dirpath, filename)
                    if os.path.getsize(file_path) <= max_file_size:
                        self.image_paths.append(file_path)
                    else:
                        print(f"Skipping oversized file: {file_path}")
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        if idx >= len(self.image_paths):
            raise IndexError("Index out of range")
            
        image_path = self.image_paths[idx]
        
        # Validate file path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        # Verify file size
        if os.path.getsize(image_path) > self.max_file_size:
            raise ValueError("Image file exceeds maximum allowed size")
            
        # Read and preprocess image
        try:
            with Image.open(image_path) as img:
                img = img.convert('RGB')  # Ensure RGB format
                if self.transform:
                    img = self.transform(img)
                return img
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4,
    pin_memory: bool = True
) -> DataLoader:
    """
    Create a secure DataLoader for the given dataset
    
    Args:
        dataset: The custom dataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of worker processes for DataLoader
        pin_memory: Whether to pin memory for faster data transfer
        
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
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,  # Shuffle for training
        drop_last=True  # Drop last incomplete batch
    )