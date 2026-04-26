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
        Secure implementation of a custom image dataset
        
        Args:
            root_dir: Root directory containing images
            transform: Optional transform to apply to images
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
                        raise ValueError(f"File {filename} exceeds size limit")
                    self.file_list.append((filename, os.path.getsize(file_path)))
                except OSError:
                    continue  # Skip files that can't be accessed
                    
        # Apply size limit if specified
        if max_files is not None:
            self.file_list = self.file_list[:max_files]
            
        # Validate file types
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        self.file_list = [
            (name, size) for name, size in self.file_list 
            if os.path.splitext(name)[1].lower() in allowed_extensions
        ]
        
        # Create secure hash of dataset contents
        self.dataset_hash = self._create_dataset_hash()
        
        # Initialize transform if provided
        self.transform = transform
        
    def _create_dataset_hash(self) -> str:
        """Create a secure hash of dataset contents"""
        hasher = hashlib.sha256()
        for filename, _ in self.file_list:
            hasher.update(filename.encode('utf-8'))
        return hasher.hexdigest()
    
    def __len__(self):
        return len(self.file_list)
    
    def __getitem__(self, index: int) -> torch.Tensor:
        if index >= len(self.file_list):
            raise IndexError("Index out of range")
            
        filename, _ = self.file_list[index]
        
        try:
            with Image.open(os.path.join(self.root_dir, filename)) as img:
                if self.transform:
                    img = self.transform(img)
                return img
        except Exception as e:
            raise ValueError(f"Error processing image {filename}: {str(e)}")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader for the dataset
    
    Args:
        dataset: The custom dataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of worker processes for DataLoader
    """
    if not isinstance(dataset, SecureImageDataset):
        raise ValueError("Invalid dataset type")
        
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Invalid batch size")
        
    if not isinstance(num_workers, int) or num_workers < 0:
        raise ValueError("Invalid number of workers")
        
    return DataLoader(
        dataset,
        batch_size