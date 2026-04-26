import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np
from typing import List, Tuple

class SecureDataset(Dataset):
    """Secure implementation of a PyTorch Dataset class"""
    
    def __init__(self, 
                 data: np.ndarray, 
                 labels: np.ndarray, 
                 transform: callable = None):
        """
        Initialize the dataset with input data and labels
        
        Args:
            data: numpy array of input data
            labels: numpy array of labels
            transform: optional data transformation function
        """
        # Validate inputs
        if not isinstance(data, np.ndarray) or not isinstance(labels, np.ndarray):
            raise TypeError("Data and labels must be numpy arrays")
        if data.shape[0] != labels.shape[0]:
            raise ValueError("Data and labels must have same number of samples")
        if data.ndim != 2 or labels.ndim != 1:
            raise ValueError("Data must be 2D and labels must be 1D")
            
        self.data = data
        self.labels = labels
        self.transform = transform
        
    def __len__(self) -> int:
        """Return the number of samples in the dataset"""
        return len(self.data)
    
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get a sample from the dataset
        
        Args:
            index: index of the sample
            
        Returns:
            Tuple containing (sample, label)
        """
        # Validate index
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range")
            
        # Apply transform if provided
        if self.transform:
            sample = self.transform(self.data[index])
        else:
            sample = self.data[index]
            
        # Convert to PyTorch tensors
        sample = torch.tensor(sample, dtype=torch.float32)
        label = torch.tensor(self.labels[index], dtype=torch.long)
        
        return sample, label

def create_secure_dataloader(dataset: SecureDataset, 
                            batch_size: int = 32, 
                            shuffle: bool = True) -> DataLoader:
    """
    Create a secure DataLoader for the given dataset
    
    Args:
        dataset: SecureDataset instance
        batch_size: number of samples per batch
        shuffle: whether to shuffle the data between epochs
        
    Returns:
        DataLoader instance
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