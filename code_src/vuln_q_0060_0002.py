```python
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import os
from typing import Optional

class SecureDataset(Dataset):
    """
    Secure dataset class for loading and preprocessing data.
    Implements strict input validation and error handling.
    """
    def __init__(self, 
                 data_dir: str,
                 transform: Optional[transforms.Compose] = None,
                 max_size: Optional[int] = None):
        """
        Initialize dataset with strict validation.
        
        Args:
            data_dir: Directory containing data files
            transform: Optional transform to apply to samples
            max_size: Optional maximum number of samples to load
        """
        # Validate inputs
        if not isinstance(data_dir, str) or not data_dir:
            raise ValueError("Invalid data directory")
        if not os.path.isdir(data_dir):
            raise ValueError("Invalid data directory")
            
        self.data_dir = data_dir
        self.transform = transform
        self.max_size = max_size
        self.samples = self._load_samples()

    def _load_samples(self) -> list:
        """
        Securely load samples from directory.
        Implements strict validation and error handling.
        """
        samples = []
        try:
            for filename in os.listdir(self.data_dir):
                if not filename.endswith('.pt'):
                    continue
                file_path = os.path.join(self.data_dir, filename)
                if not os.path.isfile(file_path):
                    continue
                try:
                    sample = torch.load(file_path)
                    if not isinstance(sample, dict):
                        continue
                    samples.append(sample)
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error accessing data directory: {str(e)}")
            
        if self.max_size:
            samples = samples[:self.max_size]
            
        return samples

    def __len__(self) -> int:
        """
        Return number of samples.
        """
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict:
        """
        Securely retrieve sample at index.
        Implements strict input validation and error handling.
        """
        if not isinstance(idx, int) or idx < 0 or idx >= len(self):
            raise IndexError("Invalid index")
            
        sample = self.samples[idx]
        if not isinstance(sample, dict):
            raise ValueError("Invalid sample format")
            
        if self.transform:
            try:
                sample = self.transform(sample)
            except Exception as e:
                raise RuntimeError(f"Error applying transform: {str(e)}")
                
        return sample

def secure_data_loader(data_dir: str, 
                       batch_size: int = 64,
                       num_workers: int = 4,
                       transform: Optional[transforms.Compose] = None,
                       max_size: Optional[int] = None) -> DataLoader:
    """
    Securely create DataLoader with strict input validation.
    
    Args:
        data_dir: Directory containing data files
        batch_size: Number of samples per batch
        num_workers: Number of worker processes
        transform: Optional transform to apply to samples
        max_size: Optional maximum number of samples to load
        
    Returns:
        DataLoader instance
    """
    # Validate inputs
    if not isinstance(data_dir, str) or not data_dir:
        raise ValueError("Invalid data directory")
    if not os.path.isdir(data_dir):
        raise ValueError("Invalid data directory")
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("Invalid batch size")
    if not isinstance(num_workers, int) or num_workers <= 0:
        raise ValueError("Invalid number of workers")
        
    dataset = SecureDataset(data_dir, transform, max_size)
    return DataLoader(dataset, batch_size=batch_size,