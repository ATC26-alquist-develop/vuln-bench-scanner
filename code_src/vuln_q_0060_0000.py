```python
import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import hashlib
from typing import List, Tuple

class SecureImageDataset(Dataset):
    """
    Secure implementation of a custom image dataset for PyTorch.
    Includes input validation, secure file handling, and memory management.
    """
    def __init__(self, 
                 root_dir: str, 
                 transform: Optional[Callable] = None,
                 max_images: int = 10000):
        """
        Initialize dataset with strict validation.
        
        Args:
            root_dir: Root directory containing images
            transform: Optional transform function
            max_images: Maximum number of images to load
        """
        # Validate root directory
        if not os.path.isdir(root_dir):
            raise ValueError("Invalid root directory")
            
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths: List[str] = []
        
        # Securely load image paths
        self._load_image_paths(max_images)
        
    def _load_image_paths(self, max_images: int) -> None:
        """
        Securely load image paths with validation.
        """
        # Get all files in directory
        files = os.listdir(self.root_dir)
        
        # Validate and filter files
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                continue
                
            # Validate file path
            file_path = os.path.join(self.root_dir, file)
            if not os.path.isfile(file_path):
                continue
                
            # Validate file size (limit to prevent memory issues)
            if os.path.getsize(file_path) > 1_000_000_000:  # 1GB limit
                continue
                
            # Validate file hash (prevent malicious files)
            if not self._validate_file_hash(file_path):
                continue
                
            self.image_paths.append(file_path)
            
        # Limit number of images
        self.image_paths = self.image_paths[:max_images]

    def _validate_file_hash(self, file_path: str) -> bool:
        """
        Validate file hash to prevent malicious files.
        """
        # Calculate file hash (SHA-256)
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
                
        # Compare against known good hashes (implement your own list)
        known_good_hashes = {
            'example_hash_1': '...',
            'example_hash_2': '...',
            # Add more known good hashes
        }
        return sha256_hash.hexdigest() in known_good_hashes

    def __len__(self) -> int:
        """
        Return number of images in dataset.
        """
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        Retrieve image and label.
        
        Args:
            idx: Index of image to retrieve
            
        Returns:
            Tuple of image tensor and label (always 0)
        """
        # Validate index
        if idx < 0 or idx >= len(self):
            raise IndexError("Index out of range")
            
        # Securely load image
        img_path = self.image_paths[idx]
        try:
            with Image.open(img_path) as img:
                # Convert to RGB to ensure consistent format
                img = img.convert('RGB')
                
                # Apply transformations if provided
                if self.transform:
                    img = self.transform(img)
                    
                # Convert to tensor
                img_tensor = transforms.ToTensor()(img)
                
                return img_tensor, 0  # Label is always 0 for images
        except Exception as e:
            raise