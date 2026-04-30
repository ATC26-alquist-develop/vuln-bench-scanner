from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

def create_data_loader(dataset, batch_size=32, num_workers=4, pin_memory=True):
    return DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,  # Set to False if you don't need shuffling
        drop_last=False  # Set to True if you want to drop the last incomplete batch
    )

# ===== cell separator =====

transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
])
dataset = YourDataset(root_dir, transform=transform)

# ===== cell separator =====

from torch.utils.data import CacheDataset

class CachedDataset(Dataset):
    def __init__(self, dataset, cache_size=1000):
        self.dataset = dataset
        self.cache_size = cache_size
        self.cache = {}

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if idx in self.cache:
            return self.cache[idx]
        else:
            data = self.dataset[idx]
            if len(self.cache) >= self.cache_size:
                self.cache.pop(next(iter(self.cache)))
            self.cache[idx] = data
            return data

# ===== cell separator =====

from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
    loss = loss_fn(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()

# ===== cell separator =====

dataset = YourDataset(root_dir, transform=transform, dtype=torch.float16)

# ===== cell separator =====

import torch.cuda

def adjust_batch_size(current_batch_size, max_memory_usage_mb=1024):
    while True:
        try:
            with torch.cuda.device(0):
                with torch.no_grad():
                    data_loader = create_data_loader(dataset, batch_size=current_batch_size)
                    for batch in data_loader:
                        _ = batch[0].sum().item()
                        torch.cuda.empty_cache()
                        if torch.cuda.memory_allocated() > max_memory_usage_mb * 1024 * 1024:
                            return current_batch_size // 2
        except RuntimeError as e:
            if "CUDA out of memory" in str(e):
                return current_batch_size // 2
            else:
                raise e
        current_batch_size = max(current_batch_size // 2, 1)
    return current_batch_size