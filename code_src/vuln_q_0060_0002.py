import torch
from torch.utils.data import DataLoader, Dataset
import os
from typing import Optional
import hashlib
import logging

class SecureDataset(Dataset):
    """
    Secure implementation of a PyTorch Dataset.
    """
    def __init__(self, data_path: str, transform: Optional[callable] = None):
        """
        Initialize dataset with validation and error handling.
        
        Args:
            data_path: Path to the dataset
            transform: Optional transformation function
        """
        # Validate input
        if not isinstance(data_path, str) or not data_path:
            raise ValueError("data_path must be a non-empty string")
        
        # Validate file exists and is a file
        if not os.path.isfile(data_path):
            raise FileNotFoundError(f"Dataset file not found: {data_path}")
        
        # Validate file size (e.g., not larger than 1GB)
        if os.path.getsize(data_path) > 1_000_000_000:  # 1GB limit
            raise ValueError(f"Dataset file too large: {data_path}")
            
        self.data_path = data_path
        self.transform = transform
        self._data = self._load_data()
        
    def _load_data(self) -> list:
        """
        Securely load data from file.
        """
        try:
            with open(self.data_path, 'rb') as f:
                # Read file in chunks to handle large files
                data = []
                while True:
                    chunk = f.read(8192)  # Read 8KB at a time
                    if not chunk:
                        break
                    data.extend(chunk)
                return list(data)
        except Exception as e:
            logging.error(f"Error loading dataset: {str(e)}")
            raise

    def __len__(self) -> int:
        """Return number of items in dataset."""
        return len(self._data)

    def __getitem__(self, idx: int) -> torch.Tensor:
        """
        Get item at index with validation.
        
        Args:
            idx: Index of the item to retrieve
            
        Returns:
            Preprocessed tensor
        """
        try:
            # Validate index
            if not isinstance(idx, int) or idx < 0 or idx >= len(self):
                raise IndexError("Index out of bounds")
                
            # Load data for this item
            item = self._data[idx]
            
            # Convert to tensor
            tensor = torch.tensor(item, dtype=torch.float32)
            
            # Apply transformation if provided
            if self.transform:
                tensor = self.transform(tensor)
                
            return tensor
        except Exception as e:
            logging.error(f"Error retrieving item: {str(e)}")
            raise

def create_dataloader(
    dataset: SecureDataset,
    batch_size: int = 32,
    num_workers: int = 4,
    shuffle: bool = True
) -> DataLoader:
    """
    Create a secure DataLoader with validation.
    
    Args:
        dataset: SecureDataset instance
        batch_size: Size of batches
        num_workers: Number of worker processes
        shuffle: Whether to shuffle data
        
    Returns:
        DataLoader instance
    """
    # Validate inputs
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")
        
    if not isinstance(num_workers, int) or num_workers <= 0:
        raise ValueError("num_workers must be a positive integer")
        
    # Create DataLoader with secure settings
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True,  # Enable pinned memory for better performance
        prefetch_factor=2,  # Optimize data loading
        drop_last=False