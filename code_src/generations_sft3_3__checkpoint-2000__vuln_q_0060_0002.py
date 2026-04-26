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
            max_memory_mb: Maximum allowed memory usage in MB
        """
        self.data_path = data_path
        self.batch_size = batch_size
        self.max_memory_mb = max_memory_mb
        
        # Validate inputs
        if not isinstance(data_path, str) or not data_path:
            raise ValueError("Invalid data path")
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("Invalid batch size")
        if not isinstance(max_memory_mb, int) or max_memory_mb <= 0:
            raise ValueError("Invalid memory limit")
            
    def _validate_file(self) -> None:
        """Validate file exists and has proper permissions"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        if not os.access(self.data_path, os.R_OK):
            raise PermissionError(f"No read access to file: {self.data_path}")

    def _secure_load(self) -> torch.Tensor:
        """Securely load data with memory limits"""
        try:
            # Load data using numpy for memory efficiency
            data = np.load(self.data_path)
            
            # Validate data type
            if not isinstance(data, np.ndarray):
                raise ValueError("Invalid data format")
                
            # Convert to PyTorch tensor with proper type
            tensor = torch.from_numpy(data).float()
            
            # Check tensor size
            if tensor.numel() > 1_000_000_000:  # 1GB limit
                raise ValueError("Data too large")
                
            return tensor
            
        except Exception as e:
            raise RuntimeError(f"Error loading data: {str(e)}")

    def __iter__(self) -> torch.Tensor:
        """Secure iterator for data loading"""
        self._validate_file()
        self.data = self._secure_load()
        
        # Ensure data is on CPU for memory safety
        self.data = self.data.to('cpu')
        
        # Create secure batch generator
        for i in range(0, len(self.data), self.batch_size):
            yield self.data[i:i+self.batch_size]

    def __len__(self) -> int:
        """Return number of samples"""
        return len(self.data)