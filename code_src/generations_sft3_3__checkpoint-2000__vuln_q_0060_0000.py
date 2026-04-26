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
        max_files: int = 10000
    ) -> None:
        """
        Secure implementation of a custom image dataset.
        
        Args:
            image_dir: Directory containing images
            transform: Optional transform to be applied to images
            max_files: Maximum number of files to load (prevents memory issues)
        """
        super().__init__()
        
        # Validate and sanitize input paths
        self.image_dir = os.path.abspath(image_dir)
        if not os.path.exists(self.image_dir):
            raise ValueError("Image directory does not exist")
            
        self.transform = transform
        self.max_files = max_files
        
        # Securely list files with proper error handling
        try:
            self.file_list = [
                f for f in os.listdir(self.image_dir)
                if os.path.isfile(os.path.join(self.image_dir, f))
            ][:max_files]
        except Exception as e:
            logging.error(f"Error listing files: {str(e)}")
            raise ValueError("Unable to access image files")
            
        # Validate file extensions
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        self.file_list = [
            f for f in self.file_list 
            if os.path.splitext(f)[1].lower() in valid_extensions
        ]
        
        if not self.file_list:
            raise ValueError("No valid image files found")

    def __len__(self) -> int:
        """Return number of images in dataset"""
        return len(self.file_list)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        """
        Get item from dataset with proper error handling and validation
        """
        if index < 0 or index >= len(self.file_list):
            raise IndexError("Index out of range")
            
        try:
            image_path = os.path.join(self.image_dir, self.file_list[index])
            with Image.open(image_path) as img:
                # Apply transform if provided
                if self.transform:
                    img = self.transform(img)
                return img, 0  # Assuming 0 as label for now
                
        except Exception as e:
            logging.error(f"Error processing image {index}: {str(e)}")
            raise ValueError("Unable to process image")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader with proper error handling
    """
    try:
        return DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
            drop_last=True
        )
    except Exception as e:
        logging.error(f"Error creating DataLoader: {str(e)}")
        raise ValueError("Unable to create DataLoader")