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
        max_files: int = 1000000,
        allowed_extensions: List[str] = ['.jpg', '.jpeg', '.png']
    ):
        """
        Secure implementation of a custom image dataset
        
        Args:
            root_dir: Root directory containing images
            transform: Optional transform to be applied to images
            max_files: Maximum number of files allowed in dataset
            allowed_extensions: List of allowed file extensions
        """
        super().__init__()
        
        # Validate and sanitize input paths
        self.root_dir = os.path.abspath(root_dir)
        if not os.path.exists(self.root_dir):
            raise ValueError("Root directory does not exist")
            
        # Validate and sanitize transform
        if transform is None:
            self.transform = transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
            ])
        else:
            self.transform = transform
            
        # Validate allowed extensions
        if not all(ext.lower() in allowed_extensions for ext in allowed_extensions):
            raise ValueError("Invalid file extension")
            
        # Get list of files with size limit
        self.file_list: List[Tuple[str, int]] = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if len(self.file_list) >= max_files:
                    raise ValueError(f"Maximum file limit ({max_files}) exceeded")
                if any(file.lower().endswith(ext) for ext in allowed_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > 100_000_000:  # 100MB limit
                            continue
                        self.file_list.append((file_path, file_size))
                    except OSError:
                        continue

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, index: int) -> torch.Tensor:
        file_path, _ = self.file_list[index]
        
        try:
            with Image.open(file_path) as img:
                img = self.transform(img)
                return img
        except Exception as e:
            raise ValueError(f"Error processing image {file_path}: {str(e)}")

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
    
    Returns:
        DataLoader instance
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
        pin_memory=True,
        persistent_workers=True
    )