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
            raise ValueError("Unsupported file format")
            
        # Read and validate data
        try:
            self.data = pd.read_csv(file_path, nrows=1000000)  # Limit to first 1M rows
        except Exception as e:
            raise ValueError(f"Failed to read dataset: {str(e)}")
            
        # Ensure required columns exist
        required_columns = ['id', 'feature1', 'feature2']  # Add your required columns
        if not all(col in self.data.columns for col in required_columns):
            raise ValueError("Dataset missing required columns")
            
        # Convert to PyTorch tensors
        self.data['id'] = self.data['id'].astype('int64')
        self.data['feature1'] = self.data['feature1'].astype('float32')
        self.data['feature2'] = self.data['feature2'].astype('float32')
        
        self.batch_size = min(batch_size, 1024)  # Limit batch size
        self.shuffle = shuffle
        self.num_workers = min(num_workers, 4)  # Limit workers
        
        # Create DataLoader with security controls
        self.dataloader = DataLoader(
            self.data,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            num_workers=self.num_workers,
            pin_memory=True,
            drop_last=True
        )

    def __len__(self):
        """Return number of samples"""
        return len(self.data)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get batch with security controls"""
        if index >= len(self):
            raise IndexError("Index out of range")
            
        batch = next(iter(self.dataloader))
        return batch['feature1'].to(torch.float32), batch['feature2'].to(torch.float32)

def load_dataset(file_path: str) -> SecureDataset:
    """Secure wrapper to load dataset"""
    return SecureDataset(file_path)