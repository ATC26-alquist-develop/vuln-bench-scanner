import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np
from typing import List, Tuple

class SecureDataset(Dataset):
    """Secure implementation of a PyTorch Dataset class"""
    
    def __init__(self, data: List[np.ndarray], labels: List[np.ndarray], 
                 transform: callable = None):
        """
        Initialize the dataset with validation against type hints
        
        Args:
            data: List of numpy arrays containing the input data
            labels: List of numpy arrays containing the labels
            transform: Optional callable for data augmentation
        """
        # Validate inputs
        if not isinstance(data, list) or not isinstance(labels, list):
            raise TypeError("Data and labels must be lists")
            
        if len(data) != len(labels):
            raise ValueError("Data and labels must have the same length")
            
        # Convert to numpy arrays if not already
        self.data = np.array(data, dtype=np.float32)
        self.labels = np.array(labels, dtype=np.int64)
        
        # Validate transform
        if transform is not None:
            if not callable(transform):
                raise TypeError("Transform must be callable")
            self.transform = transform
        else:
            self.transform = None

    def __len__(self) -> int:
        """Return the number of samples in the dataset"""
        return len(self.data)

    def __getitem__(self, index: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a sample from the dataset
        
        Args:
            index: Index of the sample to retrieve
            
        Returns:
            Tuple containing the sample data and label
            
        Raises:
            IndexError: If index is out of range
        """
        # Validate index
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range")
            
        # Apply transform if provided
        if self.transform:
            sample = self.transform(self.data[index])
        else:
            sample = self.data[index]
            
        return sample, self.labels[index]

def create_secure_dataloader(dataset: SecureDataset, 
                            batch_size: int = 32, 
                            shuffle: bool = True) -> DataLoader:
    """
    Create a secure DataLoader instance
    
    Args:
        dataset: The dataset to load
        batch_size: Number of samples per batch
        shuffle: Whether to shuffle data between epochs
        
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
        num_workers=0,  # Limit to CPU only for security
        pin_memory=False,  # Disable pinning for security
        drop_last=False  # Prevent memory issues
    )