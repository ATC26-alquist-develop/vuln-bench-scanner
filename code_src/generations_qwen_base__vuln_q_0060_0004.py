from torch.utils.data import DataLoader, Dataset
from torch.utils.data.dataloader import DataLoader

class MyDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Assuming `train_data` and `train_labels` are your datasets
train_dataset = MyDataset(train_data, train_labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

# ===== cell separator =====

from torchvision import transforms

transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_dataset = MyDataset(train_data, train_labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4, pin_memory=True, drop_last=True, transform=transform)

# ===== cell separator =====

import torch.nn as nn
import torch.distributed as dist

model = nn.Sequential(nn.Linear(100, 50), nn.ReLU(), nn.Linear(50, 10))
model = nn.parallel.DistributedDataParallel(model, device_ids=[rank])

# Assuming `train_loader` is your distributed DataLoader

# ===== cell separator =====

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4, pin_memory=True, prefetch_factor=2)