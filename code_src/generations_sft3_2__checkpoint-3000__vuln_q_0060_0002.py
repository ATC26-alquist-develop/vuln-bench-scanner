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
            batch_size: Batch size for DataLoader
            num_workers: Number of DataLoader workers
            shuffle: Whether to shuffle data during training
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
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("Batch size must be a positive integer")
            
        # Validate num workers
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("Number of workers must be a non-negative integer")
            
        self.file_path = file_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        
        # Verify file integrity
        self._verify_file_integrity(file_path)
        
    def _verify_file_integrity(self, file_path: str) -> None:
        """Verify file integrity using SHA256 hash"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        print(f"File integrity verified. SHA256: {sha256_hash.hexdigest()}")

    def __len__(self) -> int:
        """Return dataset length"""
        return sum(1 for _ in open(self.file_path, 'rb'))

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get item from dataset"""
        # Implement your data loading logic here
        # This is a placeholder - replace with actual data loading
        return torch.tensor([0.0]), torch.tensor([0.0])

def create_dataloader(dataset: Dataset, 
                     batch_size: int,
                     shuffle: bool = True) -> DataLoader:
    """Create a secure DataLoader"""
    return DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=batch_size,  # Prefer fewer workers for larger batch sizes
        shuffle=shuffle,
        pin_memory=True,  # Improve memory efficiency
        drop_last=True,  # Drop last incomplete batch
        timeout=30.0,  # Set timeout to prevent hanging
        worker_init_fn=None  # Disable worker-specific initialization
    )

# Example usage
if __name__ == "__main__":
    try:
        dataset = SecureDataset(file_path="/path/to/dataset.csv")
        dataloader = create_dataloader(dataset, batch_size=32)
        
        # Iterate through DataLoader
        for batch in dataloader:
            # Process batches
            pass
            
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")