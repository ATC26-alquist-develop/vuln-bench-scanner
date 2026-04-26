import torch
from torch.utils.data import DataLoader, Dataset
from typing import List, Optional
import os

class SecureCustomDataset(Dataset):
    def __init__(self, 
                 data_dir: str,
                 transform: Optional[callable] = None,
                 max_files: int = 1000) -> None:
        """
        Secure implementation of a custom dataset for PyTorch DataLoader
        
        Args:
            data_dir: Directory containing dataset files
            transform: Optional data transformation function
            max_files: Maximum number of files to load (prevents resource exhaustion)
        """
        super().__init__()
        
        # Validate and sanitize input paths
        self.data_dir = os.path.abspath(data_dir)
        if not os.path.exists(self.data_dir):
            raise ValueError("Data directory does not exist")
            
        # Validate file extensions
        allowed_extensions = {'.txt', '.csv', '.json'}
        self.file_list = []
        for filename in os.listdir(self.data_dir):
            if os.path.splitext(filename)[1].lower() in allowed_extensions:
                self.file_list.append(os.path.join(self.data_dir, filename))
                
        # Limit number of files to prevent resource exhaustion
        self.file_list = self.file_list[:max_files]
        
        # Initialize transform if provided
        self.transform = transform
        
    def __len__(self) -> int:
        """Return the number of samples in the dataset"""
        return len(self.file_list)
    
    def __getitem__(self, index: int) -> dict:
        """
        Get a sample from the dataset
        
        Args:
            index: Index of the sample to retrieve
            
        Returns:
            Dictionary containing the sample data and optionally transformed data
            
        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index >= len(self.file_list):
            raise IndexError("Index out of range")
            
        # Read file contents securely
        file_path = self.file_list[index]
        try:
            with open(file_path, 'r') as f:
                data = f.read()
                
            # Apply transformation if provided
            if self.transform:
                data = self.transform(data)
                
            return {'data': data}
            
        except Exception as e:
            raise RuntimeError(f"Error reading file {file_path}: {str(e)}")

def create_secure_dataloader(dataset: SecureCustomDataset, 
                            batch_size: int,
                            num_workers: int = 0) -> DataLoader:
    """
    Create a secure DataLoader for the custom dataset
    
    Args:
        dataset: SecureCustomDataset instance
        batch_size: Number of samples per batch
        num_workers: Number of worker processes to use
        
    Returns:
        DataLoader instance
        
    Raises:
        ValueError: If batch_size is invalid
    """
    if not isinstance(dataset, SecureCustomDataset):
        raise ValueError("Dataset must be an instance of SecureCustomDataset")
        
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Batch size must be a positive integer")
        
    if num_workers < 0:
        raise ValueError("Number of workers must be non-negative")
        
    return DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True
    )