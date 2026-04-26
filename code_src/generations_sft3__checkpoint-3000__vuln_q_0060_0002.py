```python
import os
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple
import hashlib

class SecureDataset(Dataset):
    """Secure implementation of a PyTorch dataset"""
    
    def __init__(self, 
                 file_path: str,
                 max_file_size: int = 1024 * 1024 * 100,  # 100MB limit
                 batch_size: int = 32,
                 shuffle: bool = True,
                 num_workers: int = 2):
        """
        Initialize dataset with security controls
        
        Args:
            file_path: Path to dataset file
            max_file_size: Maximum allowed file size in bytes
            batch_size: Batch size for DataLoader
            shuffle: Whether to shuffle data
            num_workers: Number of DataLoader workers
        """
        super().__init__()
        
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
            
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_file_size} bytes")
            
        # Validate file extension
        allowed_extensions = {'.csv', '.parquet', '.json'}
        if not os.path.splitext(file_path)[1].lower() in allowed_extensions:
            raise ValueError("Unsupported file format. Only .csv, .parquet, and .json are allowed")
            
        # Read and validate data
        try:
            self.data = pd.read_csv(file_path, nrows=1000000)  # Limit to first 1M rows
        except Exception as e:
            raise ValueError(f"Failed to read dataset: {str(e)}")
            
        # Validate data
        if self.data.empty:
            raise ValueError("Empty dataset")
            
        # Set up DataLoader with security controls
        self.loader = DataLoader(
            self,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=True,
            drop_last=True
        )
        
    def __len__(self):
        """Return number of samples"""
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get item securely with validation
        
        Args:
            idx: Index of item
            
        Returns:
            Tuple of (features, labels)
        """
        # Validate index
        if not isinstance(idx, int) or idx < 0 or idx >= len(self):
            raise IndexError("Invalid index")
            
        # Get row as dictionary
        row = self.data.iloc[idx].to_dict()
        
        # Convert to PyTorch tensors
        features = torch.tensor(row['features'], dtype=torch.float32)
        labels = torch.tensor(row['labels'], dtype=torch.long)
        
        return features, labels

def load_dataset(file_path: str, 
                 max_file_size: int = 1024 * 1024 * 100,
                 batch_size: int = 32,
                 shuffle: bool = True,
                 num_workers: int = 2) -> DataLoader:
    """
    Securely load and preprocess dataset
    
    Args:
        file_path: Path to dataset file
        max_file_size: Maximum allowed file size in bytes
        batch_size: Batch size for DataLoader
        shuffle: Whether to shuffle data
        num_workers: Number of DataLoader workers
        
    Returns:
        DataLoader instance
    """
    # Validate file path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
    # Create and validate dataset
    try:
        dataset = Secure