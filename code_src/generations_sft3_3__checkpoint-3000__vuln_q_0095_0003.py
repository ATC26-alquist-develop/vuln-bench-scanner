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
            pin_memory: Whether to copy Tensors into CUDA pinned memory
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

        # Validate dataset samples
        for sample in dataset:
            if not isinstance(sample, dict):
                raise ValueError("Dataset samples must be dictionaries")
            if not all(isinstance(v, (int, float, str, bool)) for v in sample.values()):
                raise ValueError("Dataset samples must contain only basic data types")

        # Create DataLoader with validated parameters
        self.data_loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=pin_memory,
            drop_last=drop_last,
            collate_fn=self._secure_collate
        )

    @staticmethod
    def _secure_collate(batch):
        """
        Secure collate function to handle batch conversion
        
        Args:
            batch: Batch of samples
            
        Returns:
            Tuple of (batched inputs, batched targets) if available
        """
        if not batch:
            return [], []
            
        if not isinstance(batch[0], dict):
            raise ValueError("Batch must contain dictionaries")
            
        inputs = [item['input'] for item in batch]
        targets = [item['target'] for item in batch]
        
        return inputs, targets

    def __iter__(self):
        return iter(self.data_loader)

    def __len__(self):
        return len(self.data_loader)