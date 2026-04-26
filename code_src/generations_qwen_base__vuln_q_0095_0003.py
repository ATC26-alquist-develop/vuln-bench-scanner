import os
import torch
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = self._get_samples()

    def _get_samples(self):
        # Implement this method to load your dataset
        # For example, you might load images from a directory
        # and return a list of tuples (image_path, label)
        pass

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        # Implement this method to load and preprocess a single sample
        # For example, you might load an image, apply transformations,
        # and return it along with the corresponding label
        pass

# ===== cell separator =====

def __getitem__(self, idx):
    sample = self.samples[idx]
    image_path, label = sample

    # Load the image
    image = Image.open(image_path).convert('RGB')

    # Apply transformations
    if self.transform:
        image = self.transform(image)

    return image, label

# ===== cell separator =====

import torchvision.transforms as transforms
from torchvision import datasets

# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Create the dataset
data_dir = 'path/to/your/dataset'
dataset = CustomDataset(data_dir, transform=transform)

# ===== cell separator =====

from torch.utils.data import DataLoader

# Create the DataLoader
batch_size = 32
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4)

# ===== cell separator =====

for batch_idx, (data, target) in enumerate(dataloader):
    print(f"Batch {batch_idx}: Data shape {data.shape}, Target shape {target.shape}")
    # Do something with the data and target