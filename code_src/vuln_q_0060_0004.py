from torch.utils.data import DataLoader
from torchvision import datasets, transforms

train_dataset = datasets.ImageFolder(root='path/to/train', 
                                    transform=transforms.Compose([
                                        transforms.Resize(256),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                                             std=[0.229, 0.224, 0.225])
                                    ]))

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, 
                           num_workers=4, pin_memory=True)

# ===== cell separator =====

import torch
import random
import numpy as np

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)

# ===== cell separator =====

from functools import lru_cache

@lru_cache(maxsize=1000)
def load_image(image_path):
    # Your image loading logic here
    pass

# ===== cell separator =====

from torch.utils.data import DataLoader

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, 
                           num_workers=4, pin_memory=True, 
                           prefetch_factor=2)