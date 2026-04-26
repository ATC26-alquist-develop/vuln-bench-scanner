from torch.utils.data import DataLoader
from typing import List, Optional
import torch

class SecureDataLoader:
    def __init__(
        self,
        dataset: List[dict],
        batch_size: int = 32,
        shuffle: bool = False,
        num_workers: int = 0,
        pin_memory: bool = False,
        drop_last: bool = False
    ):
        """
        Secure implementation of DataLoader with strict validation and safety checks
        
        Args:
            dataset: List of dictionaries containing data samples
            batch_size: Number of samples per batch
            shuffle: Whether to shuffle data before batching
            num_workers: Number of subprocesses to use for data loading
            pin_memory: Whether to pin memory for faster data transfer to GPU
            drop_last: Whether to drop the last incomplete batch
        """
        # Validate inputs
        if not isinstance(dataset, list) or not dataset:
            raise ValueError("Dataset must be a non-empty list")
            
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("Batch size must be a positive integer")
            
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("Number of workers must be a non-negative integer")
            
        if not isinstance(drop_last, bool):
            raise ValueError("drop_last must be a boolean")

        # Store validated parameters
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.drop_last = drop_last

        # Validate dataset samples
        if not all(isinstance(sample, dict) for sample in dataset):
            raise ValueError("Dataset must contain only dictionary samples")

        # Validate all samples have required keys
        required_keys = {'input', 'target'}
        if not all(required_keys.issubset(sample.keys()) for sample in dataset):
            raise ValueError("All dataset samples must contain 'input' and 'target' keys")

    def __len__(self):
        """Return the number of samples in the dataset"""
        return len(self.dataset)

    def __iter__(self):
        """Create an iterator for the DataLoader"""
        # Create a DataLoader instance with validated parameters
        data_loader = DataLoader(
            dataset=self.dataset,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            drop_last=self.drop_last
        )
        
        # Return an iterator over batches
        return iter(data_loader)

    def get_sample(self, index: int) -> dict:
        """
        Get a single sample from the dataset
        
        Args:
            index: Index of the sample to retrieve
            
        Returns:
            Dictionary containing the sample data
            
        Raises:
            IndexError: If index is out of range
        """
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")
            
        if index < 0 or index >= len(self.dataset):
            raise IndexError("Index out of range")
            
        return self.dataset[index]