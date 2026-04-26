import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

# ===== cell separator =====

class CustomDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_paths = [os.path.join(image_dir, img) for img in os.listdir(image_dir)]
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image

# ===== cell separator =====

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ===== cell separator =====

dataset = CustomDataset(image_dir='path/to/images', transform=transform)

# ===== cell separator =====

dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

# ===== cell separator =====

for images in dataloader:
    # Perform training operations on the images
    pass