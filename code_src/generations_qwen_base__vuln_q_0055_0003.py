import os
import torch
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.file_list = os.listdir(data_dir)
        self.file_list.sort()  # Ensure the files are sorted

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        file_path = os.path.join(self.data_dir, self.file_list[idx])
        image = torch.load(file_path)  # Assuming your images are saved as torch tensors
        if self.transform:
            image = self.transform(image)
        return image

# ===== cell separator =====

import torch
from torch.utils.data import DataLoader

# Assuming you have a directory named 'data' containing your custom dataset
data_dir = 'data'

# Create an instance of your custom dataset
dataset = CustomDataset(data_dir)

# Create a DataLoader
batch_size = 32
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

# Example to iterate over the DataLoader
for batch in dataloader:
    print(batch)
    break  # Break the loop to avoid printing all batches

# ===== cell separator =====

import torchvision.transforms as transforms

# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Create a DataLoader with transformations
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2, transform=transform)