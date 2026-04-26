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
        files = [f for f in os.listdir(self.data_dir) 
                 if os.path.splitext(f)[1].lower() in allowed_extensions]
        
        # Limit number of files to prevent resource exhaustion
        self.files = files[:max_files]
        
        # Initialize transform if provided
        self.transform = transform
        
        # Initialize dataset with file paths
        self.file_paths = [os.path.join(self.data_dir, f) for f in self.files]

    def __len__(self) -> int:
        """Return the number of samples in the dataset"""
        return len(self.file_paths)

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
        if not 0 <= index < len(self):
            raise IndexError("Index out of range")
            
        file_path = self.file_paths[index]
        
        # Read data from file (implement secure file reading logic here)
        # This is a placeholder - implement secure file reading logic
        data = self._secure_read_file(file_path)
        
        # Apply transformation if provided
        if self.transform:
            data = self.transform(data)
            
        return data

    def _secure_read_file(self, file_path: str) -> dict:
        """
        Securely read data from a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing the data
            
        Raises:
            ValueError: If file reading fails
        """
        try:
            # Implement secure file reading logic here
            # This is a placeholder - implement secure file reading logic
            with open(file_path, 'r') as f:
                data = f.read()
            return data
        except Exception as e:
            raise ValueError(f"Failed to read file {file_path}: {str(e)}")

def create_secure_dataloader(dataset: SecureCustomDataset, 
                             batch_size: int = 32,
                             shuffle: bool = True) -> DataLoader:
    """
    Create a secure DataLoader for the dataset
    
    Args:
        dataset: The custom dataset to load
        batch_size: Number of samples per batch
        shuffle: Whether to shuffle the data during training
        
    Returns:
        DataLoader instance
        
    Raises:
        ValueError: If batch_size is invalid
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")
        
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=4,  # Use 4 workers for data loading
        pin_memory=True,  # Optimize memory usage
        drop_last=True  # Drop last incomplete batch
    )