import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import os
import logging
from typing import List, Optional

class SecureDataLoader(data.Dataset):
    """Secure implementation of a data loader with strict validation"""
    
    def __init__(self, 
                 data_dir: str,
                 transform: Optional[transforms.Compose] = None,
                 batch_size: int = 32,
                 num_workers: int = 4):
        """
        Initialize secure data loader
        
        Args:
            data_dir: Directory containing the dataset
            transform: Optional transform to apply to the data
            batch_size: Batch size for DataLoader
            num_workers: Number of workers for DataLoader
        """
        super().__init__()
        
        # Validate inputs
        if not os.path.exists(data_dir):
            raise ValueError("Data directory does not exist")
            
        # Set up secure transforms
        self.transform = transform or transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        # Load dataset
        self.dataset = CIFAR10(root=data_dir, 
                               train=True, 
                               download=True,
                               transform=self.transform)
        
        # Set up secure DataLoader
        self.dataloader = DataLoader(
            self.dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
            drop_last=True
        )
        
    def __len__(self):
        """Return the number of samples in the dataset"""
        return len(self.dataset)
    
    def __getitem__(self, index: int) -> tuple:
        """Get a sample from the dataset"""
        if index >= len(self):
            raise IndexError("Index out of range")
            
        sample = self.dataset[index]
        return sample

def setup_logging():
    """Setup secure logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='data_loader.log',
        filemode='a'
    )

def main():
    """Main function to demonstrate secure data loading"""
    setup_logging()
    
    try:
        # Create secure data loader
        data_loader = SecureDataLoader(
            data_dir="/path/to/cifar10",
            batch_size=32,
            num_workers=4
        )
        
        # Iterate through data loader
        for i, (images, labels) in enumerate(data_loader):
            if i == 0:
                logging.info(f"Loaded {len(images)} samples")
            # Process data here
            break
            
    except Exception as e:
        logging.error(f"Error during data loading: {str(e)}")
        raise

if __name__ == "__main__":
    main()