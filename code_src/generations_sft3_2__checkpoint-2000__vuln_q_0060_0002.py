import torch
import torch.nn.functional as F
import numpy as np
from typing import Union, List
import os

class SecureDataLoader:
    def __init__(self, 
                 data_path: str, 
                 batch_size: int = 32, 
                 max_memory_mb: int = 1024):
        """
        Secure DataLoader with memory and security controls
        
        Args:
            data_path: Path to the dataset
            batch_size: Number of samples per batch
            max_memory_mb: Maximum allowed memory in MB
        """
        self.data_path = data_path
        self.batch_size = batch_size
        self.max_memory_mb = max_memory_mb
        self.current_batch = None
        self.current_batch_size = 0
        
    def _validate_path(self) -> bool:
        """Validate file path and permissions"""
        if not os.path.exists(self.data_path):
            raise ValueError("Dataset path does not exist")
        if not os.access(self.data_path, os.R_OK):
            raise PermissionError("No read access to dataset file")
        return True
    
    def _secure_load_chunk(self, chunk_size: int) -> Union[np.ndarray, None]:
        """Securely load data in chunks"""
        try:
            with open(self.data_path, 'rb') as f:
                f.seek(chunk_size)
                chunk = np.fromfile(f, dtype=np.float32, count=chunk_size)
                if len(chunk) != chunk_size:
                    return None
                return chunk
        except (IOError, OSError):
            return None
    
    def _secure_batch(self) -> Union[torch.Tensor, None]:
        """Securely batch data"""
        if self.current_batch is None:
            return None
            
        # Convert to PyTorch tensor with secure memory handling
        try:
            return torch.tensor(self.current_batch, 
                               dtype=torch.float32,
                               device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        except RuntimeError:
            return None
        
    def __iter__(self):
        """Secure iterator implementation"""
        self._validate_path()
        return self
    
    def __next__(self):
        """Secure next batch implementation"""
        if self.current_batch_size >= self.batch_size:
            self.current_batch_size = 0
            return self._secure_batch()
        
        # Load data in chunks
        while self.current_batch_size < self.batch_size:
            chunk = self._secure_load_chunk(self.batch_size - self.current_batch_size)
            if chunk is None:
                raise RuntimeError("Failed to load data")
                
            # Add to current batch
            self.current_batch = np.concatenate([self.current_batch, chunk])
            self.current_batch_size += len(chunk)
            
            if self.current_batch_size >= self.batch_size:
                break
                
        return self._secure_batch()