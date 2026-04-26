```python
import os
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple
import hashlib

class SecureDataset(Dataset):
    """Secure dataset class for loading and preprocessing data"""
    
    def __init__(self, 
                 file_path: str,
                 max_file_size: int = 1024 * 1024 * 100,  # 100MB limit
                 batch_size: int = 32,
                 num_workers: int = 4,
                 shuffle: bool = True,
                 seed: int = 42):
        """
        Initialize dataset with security controls
        
        Args:
            file_path: Path to the dataset file
            max_file_size: Maximum allowed file size in bytes
            batch_size: Batch size for DataLoader
            num_workers: Number of DataLoader workers
            shuffle: Whether to shuffle the dataset
            seed: Random seed for reproducibility
        """
        super().__init__()
        self.file_path = os.path.abspath(file_path)
        self.max_file_size = max_file_size
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        
        # Verify file exists and check size
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Dataset file not found: {self.file_path}")
            
        # Check file size
        file_size = os.path.getsize(self.file_path)
        if file_size > self.max_file_size:
            raise ValueError(f"File size exceeds maximum allowed size of {self.max_file_size} bytes")
            
        # Verify file is readable
        if not os.access(self.file_path, os.R_OK):
            raise PermissionError(f"No read permission for file: {self.file_path}")
            
        # Verify file extension
        allowed_extensions = {'.csv', '.parquet', '.json'}
        if not os.path.splitext(self.file_path)[1].lower() in allowed_extensions:
            raise ValueError("Unsupported file format. Only .csv, .parquet, and .json are allowed")
            
        # Load and preprocess data
        self.data = self._load_and_preprocess()
        
        # Set random seed
        torch.manual_seed(seed)
        
    def _load_and_preprocess(self) -> List[Tuple[torch.Tensor, torch.Tensor]]:
        """
        Securely load and preprocess data
        
        Returns:
            List of tuples containing (features, labels)
        """
        try:
            # Load data based on file type
            if self.file_path.lower().endswith('.csv'):
                df = pd.read_csv(self.file_path, nrows=1000000)  # Limit to first 1M rows
            elif self.file_path.lower().endswith('.parquet'):
                df = pd.read_parquet(self.file_path, engine='pyarrow')
            elif self.file_path.lower().endswith('.json'):
                df = pd.read_json(self.file_path, lines=True)
            else:
                raise ValueError("Unsupported file format")
                
            # Validate data
            if df.empty:
                raise ValueError("Empty dataset after loading")
                
            # Convert to tensors
            features = df.drop(columns=['target_column']).values.astype('float32')
            labels = df['target_column'].values.astype('int64')
            
            # Validate tensor shapes
            if features.shape[0] != labels.shape[0]:
                raise ValueError("Mismatch between features and labels")
                
            return list(zip(torch.tensor(features), torch.tensor(labels)))
            
        except Exception as e:
            raise RuntimeError(f"Error processing dataset: {str(e)}")

    def __len__(self) -> int:
        """Return number of samples"""
        return len(self.data)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]: