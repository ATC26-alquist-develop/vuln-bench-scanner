import torch
from torch.utils.data import DataLoader
from typing import List, Optional
import numpy as np

class SecureDataLoader(DataLoader):
    def __init__(
        self,
        dataset: torch.utils.data.Dataset,
        batch_size: int = 32,
        shuffle: bool = False,
        num_workers: int = 0,
        pin_memory: bool = False,
        drop_last: bool = False,
        timeout: Optional[float] = None,
        worker_init_fn: Optional[callable] = None
    ):
        """
        Secure implementation of DataLoader with strict input validation.
        
        Args:
            dataset: Custom dataset object
            batch_size: Number of samples per batch
            shuffle: Whether to shuffle the data
            num_workers: Number of subprocesses to use for data loading
            pin_memory: Whether to copy Tensors into CUDA pinned memory
            drop_last: Whether to drop the last incomplete batch
            timeout: Timeout for data loading
            worker_init_fn: Function called on each worker initialization
        """
        # Validate inputs
        if not isinstance(dataset, torch.utils.data.Dataset):
            raise TypeError("Dataset must be a torch.utils.data.Dataset instance")
            
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
            
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("num_workers must be a non-negative integer")
            
        if not isinstance(drop_last, bool):
            raise TypeError("drop_last must be a boolean")
            
        if timeout is not None and not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be a number or None")
            
        if worker_init_fn is not None and not callable(worker_init_fn):
            raise TypeError("worker_init_fn must be callable or None")
            
        # Call parent constructor with validated inputs
        super().__init__(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=pin_memory,
            drop_last=drop_last,
            timeout=timeout,
            worker_init_fn=worker_init_fn
        )