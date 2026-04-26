import torch
from torch.utils.data import DataLoader
from typing import List, Optional
import numpy as np

class SecureCustomDataset(torch.utils.data.Dataset):
    def __init__(self, data: List[dict], transform: Optional[callable] = None):
        """
        Secure implementation of a custom dataset for PyTorch DataLoader
        
        Args:
            data: List of dictionaries containing data samples
            transform: Optional callable for data transformation
        """
        # Validate input data
        if not isinstance(data, list):
            raise ValueError("Data must be a list of dictionaries")
            
        # Convert to numpy array for secure handling
        self.data = np.array(data)
        
        # Validate transform if provided
        if transform is not None:
            if not callable(transform):
                raise ValueError("Transform must be a callable")
            self.transform = transform
        else:
            self.transform = None

    def __len__(self):
        """Return the number of samples in the dataset"""
        return len(self.data)

    def __getitem__(self, index: int) -> dict:
        """
        Get a sample from the dataset
        
        Args:
            index: Index of the sample to retrieve
            
        Returns:
            Sample as a dictionary
            
        Raises:
            IndexError: If index is out of range
        """
        # Validate index
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")
            
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range")
            
        # Get sample
        sample = self.data[index]
        
        # Apply transform if provided
        if self.transform:
            sample = self.transform(sample)
            
        return sample

def create_secure_dataloader(dataset: SecureCustomDataset, batch_size: int, shuffle: bool = True) -> DataLoader:
    """
    Create a secure DataLoader for the given dataset
    
    Args:
        dataset: SecureCustomDataset instance
        batch_size: Number of samples per batch
        shuffle: Whether to shuffle the data during training
        
    Returns:
        DataLoader instance
        
    Raises:
        ValueError: If batch_size is not positive
    """
    # Validate batch size
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Batch size must be a positive integer")
        
    # Create DataLoader with security measures
    return DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,  # Limit to 0 for security
        pin_memory=False,  # Disable pin_memory for security
        drop_last=False  # Prevent data loss
    )