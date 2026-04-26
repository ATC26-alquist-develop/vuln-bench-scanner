from torch.utils.data import DataLoader
from typing import List, Optional
import torch
from torch.utils.data import Dataset
import logging

class SecureDataLoader:
    def __init__(self, dataset: Dataset, batch_size: int = 32, 
                 shuffle: bool = False, num_workers: int = 0):
        """
        Secure implementation of DataLoader with strict validation and safety checks
        
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
            raise ValueError("Batch size must be a positive integer")
        if not isinstance(shuffle, bool):
            raise ValueError("Shuffle must be a boolean value")
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("Number of workers must be a non-negative integer")
            
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
            # Create DataLoader with strict validation
            data_loader = DataLoader(
                dataset=self.dataset,
                batch_size=self.batch_size,
                shuffle=self.shuffle,
                num_workers=self.num_workers,
                pin_memory=True,  # Optimize memory usage
                drop_last=False,  # Prevent data leaks
                collate_fn=self.dataset.collate_fn  # Use dataset's collate function
            )
            
            # Validate DataLoader
            if not isinstance(data_loader, DataLoader):
                raise TypeError("Invalid DataLoader instance")
                
            return data_loader
            
        except Exception as e:
            self.logger.error(f"Error creating DataLoader: {str(e)}")
            raise