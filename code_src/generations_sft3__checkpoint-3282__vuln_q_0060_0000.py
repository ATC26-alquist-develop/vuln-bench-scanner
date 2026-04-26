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
        root_dir: str,
        transform: transforms.Compose = None,
        max_file_size: int = 1024 * 1024 * 1024,  # 1GB limit per file
        max_files: int = 1000000  # Limit total files
    ):
        """
        Initialize secure image dataset
        
        Args:
            root_dir: Root directory containing images
            transform: Optional transform for images
            max_file_size: Maximum allowed file size in bytes
            max_files: Maximum number of files allowed
        """
        super().__init__()
        
        # Validate and sanitize root directory
        if not os.path.isdir(root_dir):
            raise ValueError("Invalid root directory")
            
        self.root_dir = os.path.abspath(root_dir)
        
        # Get list of files with size validation
        self.file_list: List[Tuple[str, int]] = []
        for dirpath, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    if os.path.getsize(file_path) > max_file_size:
                        raise ValueError(f"File too large: {filename}")
                    self.file_list.append((filename, os.path.getsize(file_path)))
                except (OSError, ValueError) as e:
                    print(f"Warning: Skipping invalid file {filename}: {str(e)}")
                    continue
                    
        self.file_list.sort(key=lambda x: x[1])  # Sort by file size
        
        # Validate max files
        if len(self.file_list) > max_files:
            raise ValueError(f"Too many files in directory: {max_files}")
            
        # Initialize transform if provided
        self.transform = transform
        
    def __len__(self):
        return len(self.file_list)
    
    def __getitem__(self, idx):
        if idx >= len(self.file_list):
            raise IndexError("Index out of range")
            
        filename, _ = self.file_list[idx]
        
        try:
            # Secure image loading
            with Image.open(os.path.join(self.root_dir, filename)) as img:
                # Convert to RGB if grayscale
                if img.mode == 'L':
                    img = img.convert('RGB')
                    
                # Apply transform if provided
                if self.transform:
                    img = self.transform(img)
                    
                return img, torch.tensor(0, dtype=torch.int64)
            
        except (IOError, OSError) as e:
            print(f"Error loading image {filename}: {str(e)}")
            return None

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create secure DataLoader
    
    Args:
        dataset: Validated dataset instance
        batch_size: Batch size
        num_workers: Number of worker processes for data loading
    """
    # Validate parameters
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
        drop_last=True,
        collate_fn=collate_fn  # Custom collate function for security
    )

def collate_fn(batch):