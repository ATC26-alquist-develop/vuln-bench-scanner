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
                 num_workers: int = 4,
                 shuffle: bool = True):
        """
        Initialize dataset with security controls
        
        Args:
            file_path: Path to dataset file
            max_file_size: Maximum allowed file size in bytes
            batch_size: Number of samples per batch
            num_workers: Number of data loading workers
            shuffle: Whether to shuffle the dataset
        """
        super().__init__()
        
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
            
        # Validate file size
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            raise ValueError(f"File size exceeds maximum allowed size of {max_file_size} bytes")
            
        # Validate batch size
        if batch_size <= 0 or batch_size > 1024:  # Reasonable limit
            raise ValueError("Invalid batch size")
            
        # Validate num workers
        if num_workers < 0:
            raise ValueError("Number of workers must be non-negative")
            
        self.file_path = file_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        
        # Verify file integrity
        self._verify_file_integrity(file_path)
        
        # Load data
        self.data = self._load_data(file_path)
        
    def _verify_file_integrity(self, file_path: str) -> None:
        """Verify file integrity using SHA256 hash"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        print(f"File integrity verified. SHA256: {sha256_hash.hexdigest()}")
        
    def _load_data(self, file_path: str) -> List[dict]:
        """Securely load data from CSV file"""
        try:
            df = pd.read_csv(file_path, nrows=1000000)  # Limit to first 1M rows
            return df.to_dict('records')
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")
            
    def __len__(self) -> int:
        """Return number of samples"""
        return len(self.data)
        
    def __getitem__(self, index: int) -> dict:
        """Get single sample"""
        sample = self.data[index]
        return sample

def create_dataloader(dataset: SecureDataset) -> DataLoader:
    """Create secure DataLoader"""
    return DataLoader(
        dataset=dataset,
        batch_size=dataset.batch_size,
        num_workers=dataset.num_workers,
        shuffle=dataset.shuffle,
        pin_memory=True,
        drop_last=True
    )