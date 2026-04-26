import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np
from typing import List, Tuple

class SecureCustomDataset(Dataset):
    """A secure implementation of a custom dataset for PyTorch DataLoader."""
    
    def __init__(self, data: List[Tuple[np.ndarray, np.ndarray]], 
                 transform: callable = None):
        """
        Initialize the dataset with input data and optional transform.
        
        Args:
            data: List of tuples containing (input_data, target_data)
            transform: Optional callable for data transformation
        """
        # Validate input data types
        if not all(isinstance(item, tuple) and len(item) == 2 
                   for item in data):
            raise ValueError("Invalid data format. Expected list of tuples.")
            
        # Convert to numpy arrays for secure handling
        self.data = [np.array(item[0], dtype=np.float32), 
                     np.array(item[1], dtype=np.float32)]
        
        # Validate transform if provided
        if transform is not None:
            if not callable(transform):
                raise ValueError("Transform must be a callable function")
            self.transform = transform
        else:
            self.transform = None

    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        return len(self.data[0])

    def __getitem__(self, index: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a sample from the dataset by index.
        
        Args:
            index: Index of the sample to retrieve
            
        Returns:
            Tuple of (input_data, target_data)
        """
        # Validate index
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")
            
        # Apply transform if provided
        if self.transform:
            return self.transform(self.data[0][index], self.data[1][index])
            
        return self.data[0][index], self.data[1][index]

def create_secure_dataloader(dataset: SecureCustomDataset, 
                             batch_size: int = 32,
                             shuffle: bool = True) -> DataLoader:
    """
    Create a secure DataLoader for the given dataset.
    
    Args:
        dataset: The custom dataset to load
        batch_size: Number of samples per batch
        shuffle: Whether to shuffle the data during iteration
        
    Returns:
        DataLoader instance for the dataset
    """
    # Validate batch size
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Batch size must be a positive integer")
        
    # Create DataLoader with security measures
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,  # Limit to 0 for security
        pin_memory=False,  # Disable pin_memory for security
        drop_last=False  # Prevent data leaks
    )