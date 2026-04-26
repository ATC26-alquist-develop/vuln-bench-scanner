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
                 num_workers: int = 2,
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
        if batch_size <= 0 or batch_size > 1024:  # Reasonable limit
            raise ValueError("Batch size must be between 1 and 1024")
            
        # Validate num workers
        if num_workers < 0 or num_workers > 4:
            raise ValueError("Number of workers must be between 0 and 4")
            
        # Read and validate data
        try:
            self.data = pd.read_csv(file_path, 
                                   low_memory=False,  # Handle large files
                                   encoding='utf-8')
            
            # Validate data types and content
            if not all(self.data.dtypes.apply(lambda x: pd.api.types.is_numeric_dtype(x) or 
                                              pd.api.types.is_string_dtype(x))).all():
                raise ValueError("Invalid data types detected in dataset")
                
        except Exception as e:
            raise ValueError(f"Error reading dataset: {str(e)}")
            
        # Create DataLoader with security controls
        self.loader = DataLoader(
            self,
            batch_size=batch_size,
            num_workers=num_workers,
            shuffle=shuffle,
            pin_memory=True,  # Optimize memory usage
            drop_last=True,   # Handle large datasets
            collate_fn=self.collate_fn
        )
        
    def __len__(self) -> int:
        """Return number of samples in dataset"""
        return len(self.data)
    
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get batch of samples"""
        try:
            # Validate index
            if not isinstance(index, int) or index < 0 or index >= len(self.data):
                raise IndexError("Invalid index")
                
            # Get sample
            sample = self.data.iloc[index]
            
            # Convert to tensors with type checking
            return (
                torch.tensor(sample['features'].values, dtype=torch.float32),
                torch.tensor(sample['labels'].values, dtype=torch.long)
            )
            
        except Exception as e:
            raise ValueError(f"Error processing sample at index {index}: {str(e)}")
            
    @staticmethod
    def collate_fn(batch: List[Tuple[torch.Tensor, torch.Tensor]]) -> Tuple[torch.Tensor, torch.Tensor]:
        """Custom collate function for DataLoader"""
        return (
            torch.stack([item[0] for item in batch]),
            torch.stack([item[1] for item in batch])
        )

def load_dataset(file_path: str, 
                 max_file_size: int = 1024 *