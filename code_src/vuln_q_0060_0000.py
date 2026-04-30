import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import hashlib
import hmac
import secrets

class SecureImageDataset(Dataset):
    def __init__(self, root_dir, transform=None, max_size=1024):
        """
        Initialize secure image dataset
        """
        self.root_dir = os.path.abspath(root_dir)
        self.transform = transform
        self.max_size = max_size
        self.image_paths = self._secure_scan_directory()

    def _secure_scan_directory(self):
        """Securely scan directory for image files"""
        image_paths = []
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.lower().endswith(tuple(allowed_extensions)):
                    file_path = os.path.join(root, file)
                    if self._is_safe_path(file_path):
                        image_paths.append(file_path)
        return image_paths

    def _is_safe_path(self, path):
        """Validate path is within allowed directory"""
        abs_path = os.path.abspath(path)
        return abs_path.startswith(self.root_dir)

    def __len__(self):
        """Return number of images"""
        return len(self.image_paths)

    def __getitem__(self, idx):
        """Load and preprocess image securely"""
        img_path = self.image_paths[idx]
        try:
            with Image.open(img_path) as img:
                img.verify()  # Verify image integrity
                img = img.convert('RGB')  # Convert to RGB for consistency
                if self.transform:
                    img = self.transform(img)
                return img
        except (IOError, SyntaxError):
            raise ValueError(f"Invalid image file: {img_path}")

def create_secure_dataloader(root_dir, batch_size=32, num_workers=4, 
                             transform=None, max_size=1024):
    """
    Create secure DataLoader with safety checks
    """
    dataset = SecureImageDataset(root_dir, transform, max_size)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True, 
                      num_workers=num_workers, pin_memory=True)

# Example usage
if __name__ == "__main__":
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    dataloader = create_secure_dataloader('/path/to/images', transform=transform)
    for images in dataloader:
        # Process images securely
        pass