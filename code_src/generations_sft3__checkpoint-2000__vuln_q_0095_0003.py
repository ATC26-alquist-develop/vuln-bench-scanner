from torch.utils.data import DataLoader
from typing import List, Optional
import torch
from torch.utils.data import Dataset
import logging

class SecureDataLoader:
    def __init__(self, dataset: Dataset, batch_size: int = 32, 
                 shuffle: bool = False, num_workers: int = 0):
        """
        Secure implementation of DataLoader with strict validation and security controls
        
        Args:
            dataset: Custom dataset instance
            batch_size: Number of samples per batch
            shuffle: Whether to shuffle data before batching
            num_workers: Number of subprocesses to use for data loading
        """
        # Validate inputs
        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset must be an instance of torch.utils.data.Dataset")
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        if not isinstance(shuffle, bool):
            raise TypeError("shuffle must be a boolean")
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("num_workers must be a non-negative integer")
            
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __call__(self) -> DataLoader:
        """
        Create and return a secure DataLoader instance
        
        Returns:
            torch.utils.data.DataLoader: Secure DataLoader instance
        """
        try:
            # Create DataLoader with security controls
            data_loader = DataLoader(
                dataset=self.dataset,
                batch_size=self.batch_size,
                shuffle=self.shuffle,
                num_workers=self.num_workers,
                pin_memory=True,  # Optimize memory usage
                drop_last=True,    # Handle uneven dataset sizes
                collate_fn=self.collate_fn  # Custom collate function
            )
            
            return data_loader
            
        except Exception as e:
            self.logger.error(f"Error creating DataLoader: {str(e)}")
            raise

    def collate_fn(self, batch: List[torch.Tensor]) -> torch.Tensor:
        """
        Custom collate function to handle batch data securely
        
        Args:
            batch: List of tensors to collate
            
        Returns:
            torch.Tensor: Collated batch
            
        Raises:
            ValueError: If batch is empty or contains invalid data
        """
        if not batch:
            raise ValueError("Batch cannot be empty")
            
        # Validate tensor types and shapes
        if not all(isinstance(x, torch.Tensor) for x in batch):
            raise ValueError("All elements in batch must be torch.Tensor")
            
        # Check for valid tensor shapes
        if not all(x.shape == batch[0].shape for x in batch):
            raise ValueError("All tensors in batch must have the same shape")
            
        return torch.stack(batch, dim=0)