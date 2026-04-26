import torch

from torch.utils.data import Dataset, DataLoader


class CustomDataset(Dataset):

    def __init__(self, data, transform=None):

        self.data = data

        self.transform = transform


    def __len__(self):

        return len(self.data)


    def __getitem__(self, idx):

        sample = self.data[idx]

        if self.transform:

            sample = self.transform(sample)

        return sample


# Example usage:

# Assuming 'my_data' is a list of your data samples and 'my_transform' is a transformation function

dataset = CustomDataset(my_data, transform=my_transform)

dataloader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=2)


# Now you can iterate over the DataLoader in your training loop

for batch in dataloader:

    # Process your batch here