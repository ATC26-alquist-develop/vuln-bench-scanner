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
        Secure implementation of DataLoader with strict input validation
        
        Args:
            dataset: List of dictionaries containing data samples
            batch_size: Number of samples per batch
            shuffle: Whether to shuffle data before batching
            num_workers: Number of subprocesses to use for data loading
            pin_memory: Whether to copy Tensors into CUDA pinned memory
            drop_last: Whether to drop the last incomplete batch
        """
        # Validate batch size
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        
        # Validate shuffle flag
        if not isinstance(shuffle, bool):
            raise ValueError("shuffle must be a boolean")
            
        # Validate num_workers
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("num_workers must be a non-negative integer")
            
        # Validate pin_memory flag
        if not isinstance(pin_memory, bool):
            raise ValueError("pin_memory must be a boolean")
            
        # Validate drop_last flag
        if not isinstance(drop_last, bool):
            raise ValueError("drop_last must be a boolean")
            
        # Validate dataset
        if not isinstance(dataset, list) or not dataset:
            raise ValueError("dataset must be a non-empty list of dictionaries")
            
        # Validate each sample in dataset
        for sample in dataset:
            if not isinstance(sample, dict):
                raise ValueError("Each dataset sample must be a dictionary")
            if not sample:
                raise ValueError("Each dataset sample must contain at least one key-value pair")
                
        # Store validated parameters
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.drop_last = drop_last
        
        # Create DataLoader with validated parameters
        self.data_loader = DataLoader(
            dataset=dataset,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            drop_last=self.drop_last,
            collate_fn=self._secure_collate
        )
    
    @staticmethod
    def _secure_collate(batch):
        """
        Secure collate function that handles data types safely
        
        Args:
            batch: List of samples to collate
            
        Returns:
            Tuple containing batched data and targets
        """
        # Validate batch
        if not isinstance(batch, list) or not batch:
            raise ValueError("Batch must be a non-empty list")
            
        # Validate each sample in batch
        for sample in batch:
            if not isinstance(sample, dict):
                raise ValueError("Each batch sample must be a dictionary")
            if not sample:
                raise ValueError("Each batch sample must contain at least one key-value pair")
                
        # Extract data and targets
        data = [sample['data'] for sample in batch]
        targets = [sample['target'] for sample in batch]
        
        # Convert to PyTorch tensors
        data = torch.stack(data, dim=0)
        targets = torch.stack(targets, dim=0)
        
        return data, targets