import os
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch
import logging
from typing import List, Tuple

class SecureImageDataset(Dataset):
    def __init__(
        self,
        image_dir: str,
        transform: transforms.Compose = None,
        max_files: int = 10000,
        max_file_size: int = 1024 * 1024 * 1024  # 1GB limit
    ) -> None:
        """
        Secure implementation of a custom image dataset
        
        Args:
            image_dir: Directory containing images
            transform: Optional transform for images
            max_files: Maximum number of files to load
            max_file_size: Maximum allowed file size in bytes
        """
        super().__init__()
        
        # Validate and sanitize input paths
        self.image_dir = os.path.abspath(image_dir)
        if not os.path.exists(self.image_dir):
            raise ValueError("Image directory does not exist")
            
        self.transform = transform
        self.max_files = max_files
        self.max_file_size = max_file_size
        
        # Securely list files with size limit
        self.images: List[Tuple[str, Image.Image]] = []
        try:
            for i, file in enumerate(os.listdir(self.image_dir)):
                file_path = os.path.join(self.image_dir, file)
                
                # Check file size
                if os.path.getsize(file_path) > self.max_file_size:
                    logging.warning(f"File {file} exceeds size limit")
                    continue
                    
                # Validate image
                try:
                    with Image.open(file_path) as img:
                        self.images.append((file, img))
                    
                    # Enforce file count limit
                    if len(self.images) >= self.max_files:
                        break
                except Exception as e:
                    logging.error(f"Error processing file {file}: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error accessing image directory: {str(e)}")
            raise
            
        self._validate_dataset()
        
    def _validate_dataset(self) -> None:
        """Validate dataset contents"""
        if not self.images:
            raise ValueError("No valid images found in directory")
            
    def __len__(self) -> int:
        return len(self.images)
    
    def __getitem__(self, idx: int) -> Tuple[Image.Image, Image.Image]:
        if idx >= len(self.images):
            raise IndexError("Index out of range")
            
        img_path, img = self.images[idx]
        if not img:
            raise ValueError(f"Image at index {idx} is invalid")
            
        if self.transform:
            img = self.transform(img)
            
        return img, img

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
    if not isinstance(dataset, SecureImageDataset):
        raise TypeError("Invalid dataset type")
        
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Invalid batch size")
        
    if not isinstance(num_workers, int) or num_workers < 0:
        raise ValueError("Invalid number of workers")
        
    return DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=True,
        drop_last=True,
        pin_memory=True
    )