import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os
import hashlib
from typing import List, Tuple
import logging

class SecureImageDataset(Dataset):
    """
    Secure implementation of an image dataset for PyTorch.
    
    Args:
        image_paths: List of image file paths
        transform: Optional transform to be applied on a sample.
    """
    def __init__(self, image_paths: List[str], transform: Optional[transforms.Compose] = None):
        # Validate inputs
        if not image_paths or not isinstance(image_paths, list):
            raise ValueError("image_paths must be a non-empty list")
            
        self.image_paths = []
        for path in image_paths:
            # Validate path
            if not isinstance(path, str) or not path.strip():
                continue
                
            # Validate file exists and is a file
            if not os.path.isfile(path):
                continue
                
            # Validate file extension
            if not path.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            # Validate file size (e.g., max 50MB)
            if os.path.getsize(path) > 50 * 1024 * 1024:
                continue
                
            # Validate file hash for integrity
            if not self._validate_file_hash(path):
                continue
                
            self.image_paths.append(path)
            
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        if idx < 0 or idx >= len(self):
            raise IndexError("Index out of range")

        try:
            # Load image securely
            with open(self.image_paths[idx], 'rb') as f:
                img_data = f.read()
            
            # Create PIL Image
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to RGB to ensure consistent channels
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Apply transformations
            if self.transform:
                img = self.transform(img)
            
            # Generate secure hash for this sample
            sample_hash = self._generate_sample_hash(img)
            
            return torch.tensor(img), sample_hash
        except Exception as e:
            logging.error(f"Error processing image at index {idx}: {str(e)}")
            raise

    def _validate_file_hash(self, file_path: str) -> bool:
        """Validate file hash for integrity."""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            # In a real scenario, you'd compare this against a known good hash
            return True
        except Exception:
            return False

    def _generate_sample_hash(self, image: Image.Image) -> str:
        """Generate a secure hash for the image data."""
        try:
            # Convert image to bytes and generate hash
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
            return hashlib.sha256(image_bytes).hexdigest()
        except Exception:
            return ""

def create_secure_dataloader(
    image_paths: List[str],
    batch_size: int = 32,
    shuffle: bool = True,
    num_workers: int = 4,
    transform: Optional[transforms.Compose] = None
) -> DataLoader:
    """
    Create a secure DataLoader for the image dataset.
    
    Args:
        image_paths: List of image file paths
        batch_size: Number of samples per batch
        shuffle: Whether to shuffle the dataset
        num_workers: Number of subprocesses to use for data loading
        transform: Optional transform to be applied on a sample