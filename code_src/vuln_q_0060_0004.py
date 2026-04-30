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