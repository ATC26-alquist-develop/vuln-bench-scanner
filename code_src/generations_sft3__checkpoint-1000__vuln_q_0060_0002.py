import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import os
import logging
from typing import List, Tuple

def setup_logging() -> None:
    """Set up secure logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='data_preprocessing.log',
        filemode='a'
    )

def load_and_preprocess_data(
    data_dir: str,
    batch_size: int = 32,
    num_workers: int = 4,
    pin_memory: bool = True
) -> Tuple[DataLoader, DataLoader]:
    """
    Securely load and preprocess CIFAR-10 dataset.
    
    Args:
        data_dir: Directory containing the dataset
        batch_size: Batch size for DataLoader
        num_workers: Number of workers for DataLoader
        pin_memory: Whether to pin memory for faster data transfer
    
    Returns:
        Tuple of (train_loader, test_loader)
    """
    # Setup logging
    setup_logging()
    
    try:
        # Validate inputs
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        if not isinstance(num_workers, int) or num_workers < 0:
            raise ValueError("num_workers must be a non-negative integer")
            
        # Define transformations
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        # Load dataset
        dataset = CIFAR10(
            root=data_dir,
            train=True,
            download=True,
            transform=transform
        )
        
        # Create data loaders
        train_loader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=pin_memory
        )
        
        # Create test dataset
        test_dataset = CIFAR10(
            root=data_dir,
            train=False,
            download=True,
            transform=transform
        )
        
        # Create test loader
        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=pin_memory
        )
        
        return train_loader, test_loader
        
    except Exception as e:
        logging.error(f"Error during data loading and preprocessing: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        train_loader, test_loader = load_and_preprocess_data(
            data_dir="./data",
            batch_size=32,
            num_workers=4
        )
        logging.info("Data loaded and preprocessed successfully")
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")