import torch
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Create an instance of the custom dataset
data = [1, 2, 3, 4, 5]
labels = [0, 1, 0, 1, 0]
dataset = CustomDataset(data, labels)

# Create a DataLoader
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# Iterate over the DataLoader
for batch in dataloader:
    print(batch)