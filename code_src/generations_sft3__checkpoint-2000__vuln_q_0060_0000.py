```python
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
        max_files: int = 1000000
    ) -> None:
        """
        Secure implementation of a custom image dataset
        
        Args:
            image_dir: Directory containing images
            transform: Optional transform to apply to images
            max_files: Maximum number of files to load (prevents memory issues)
        """
        super().__init__()
        
        # Validate and sanitize input paths
        self.image_dir = os.path.abspath(image_dir)
        if not os.path.exists(self.image_dir):
            raise ValueError("Image directory does not exist")
            
        self.transform = transform
        self.max_files = max_files
        
        # Securely list files with size limit
        self.file_list: List[str] = []
        for root, _, files in os.walk(self.image_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Check file size before loading
                    if os.path.getsize(file_path) > 100_000_000:  # 100MB limit
                        logging.warning(f"Skipping large file: {file_path}")
                        continue
                        
                    self.file_list.append(file_path)
                    
                    if len(self.file_list) >= self.max_files:
                        logging.info(f"Maximum file limit reached: {self.max_files}")
                        break
                except (OSError, PermissionError) as e:
                    logging.error(f"Error accessing file {file_path}: {str(e)}")
                    continue
                    
        logging.info(f"Initialized dataset with {len(self.file_list)} images")

    def __len__(self) -> int:
        """Return number of images in dataset"""
        return len(self.file_list)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        """
        Get single image with optional label
        
        Args:
            index: Index of image to retrieve
            
        Returns:
            Tuple of (image tensor, label) if available
        """
        if index >= len(self.file_list):
            raise IndexError("Index out of range")
            
        file_path = self.file_list[index]
        
        try:
            # Open image with security considerations
            with Image.open(file_path) as img:
                # Convert to RGB if grayscale
                if img.mode == 'L':
                    img = img.convert('RGB')
                    
                # Apply transforms if provided
                if self.transform:
                    img = self.transform(img)
                    
            return img, 0  # Assuming no labels for this example
            
        except (OSError, PermissionError) as e:
            logging.error(f"Error processing image {file_path}: {str(e)}")
            raise ValueError("Invalid image file")

def create_dataloader(
    dataset: SecureImageDataset,
    batch_size: int = 32,
    num_workers: int = 4
) -> DataLoader:
    """
    Create a secure DataLoader
    
    Args:
        dataset: Custom dataset instance
        batch_size: Batch size for DataLoader
        num_workers: Number of worker processes for DataLoader
        
    Returns:
        DataLoader instance
    """
    # Validate inputs
    if not isinstance(dataset, SecureImageDataset):
        raise ValueError("Invalid dataset type")
        
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Invalid batch size")
        
    if not isinstance(num_workers, int) or num_workers < 0:
        raise ValueError("Invalid number of workers")
        
    # Create DataLoader with security considerations
    return DataLoader(
        dataset,
        batch_size=batch