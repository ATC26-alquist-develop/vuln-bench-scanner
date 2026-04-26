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

train_loader = DataLoader(train_dataset, batch_size=64, 
                           shuffle=True, num_workers=4, pin_memory=True)