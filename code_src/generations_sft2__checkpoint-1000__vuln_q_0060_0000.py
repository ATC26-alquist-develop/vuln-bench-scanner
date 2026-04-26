```python
import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import hashlib
from typing import List, Tuple
import logging

class SecureImageDataset(Dataset):
    """Secure implementation of custom image dataset for PyTorch"""
    
    def __init__(self, 
                 root_dir: str,
                 transform: Optional[Callable] = None,
                 max_images: int = 10000,
                 max_file_size: int = 100 * 1024 * 1024):  # 100MB limit
        """
        Initialize secure image dataset
        
        Args:
            root_dir: Root directory containing images
            transform: Optional transform to apply to images
            max_images: Maximum number of images to load
            max_file_size: Maximum file size in bytes
        """
        # Validate inputs
        if not os.path.isdir(root_dir):
            raise ValueError("Invalid root directory")
            
        self.root_dir = root_dir
        self.transform = transform
        self.max_images = max_images
        self.max_file_size = max_file_size
        
        # Securely load image paths
        self.image_paths = self._load_image_paths()
        
    def _load_image_paths(self) -> List[str]:
        """Securely load image paths with validation"""
        image_paths = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(root, file)
                    if self._is_valid_file(file_path):
                        image_paths.append(file_path)
                        if len(image_paths) >= self.max_images:
                            break
            if len(image_paths) >= self.max_images:
                break
        return image_paths[:self.max_images]
    
    def _is_valid_file(self, file_path: str) -> bool:
        """Validate file integrity and size"""
        try:
            # Check file size
            if os.path.getsize(file_path) > self.max_file_size:
                return False
                
            # Verify file is actually an image
            with Image.open(file_path) as img:
                img.verify()
                
            # Generate secure hash for integrity check
            file_hash = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    file_hash.update(chunk)
                    
            # Log file hash for auditing
            logging.info(f"File hash: {file_hash.hexdigest()}")
            
            return True
        except Exception:
            return False
            
    def __len__(self) -> int:
        """Return number of images"""
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """Load and preprocess image"""
        if idx >= len(self):
            raise IndexError("Index out of range")
            
        file_path = self.image_paths[idx]
        try:
            with Image.open(file_path) as img:
                # Convert to RGB and apply transformations
                if self.transform:
                    img = self.transform(img)
                    
                # Convert to tensor
                img_tensor = torch.from_numpy(np.array(img)).permute(2, 0, 1)
                
                return img_tensor, idx
        except Exception as e:
            logging.error(f"Error loading image {file_path}: {str(e)}")
            raise

def create_secure_dataloader(root_dir: str, 
                             batch_size: int = 32,
                             num_workers: int = 4,
                             transform: Optional[Callable] = None) -> DataLoader:
    """
    Create secure DataLoader with validation
    
    Args:
        root_dir: Root directory containing images
        batch_size: Number of images per batch
        num_workers