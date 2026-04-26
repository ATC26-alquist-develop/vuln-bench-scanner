from torch.utils.data import DataLoader, DistributedSampler

# Assuming you have a dataset `dataset` and a sampler `sampler`
dataloader = DataLoader(dataset, batch_size=32, sampler=sampler)

# ===== cell separator =====

from torch.utils.data import DataLoader

# Assuming you have a dataset `dataset`
dataloader = DataLoader(dataset, batch_size=32, num_workers=4, pin_memory=True, prefetch_factor=2)

# ===== cell separator =====

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, file_path):
        self.data = load_data_from_file(file_path)  # Load data from file

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# ===== cell separator =====

from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = MyDataset(file_path)
dataloader = DataLoader(dataset, batch_size=32, num_workers=4, pin_memory=True, prefetch_factor=2, shuffle=True, transform=transform)