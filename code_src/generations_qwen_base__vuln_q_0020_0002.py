import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(32 * 8 * 8, 128)  # Assuming input size is 32x32
        self.fc2 = nn.Linear(128, 10)  # Assuming 10 classes

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 32 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Create an instance of the model
model = SimpleCNN()

# ===== cell separator =====

# Assuming the model is saved as 'model.pth'
model_path = 'model.pth'
model.load_state_dict(torch.load(model_path))
model.eval()  # Set the model to evaluation mode

# ===== cell separator =====

# Example input: a batch of images (batch_size, channels, height, width)
# For simplicity, we'll use a single image
input_image = torch.randn(1, 3, 32, 32)  # Assuming input size is 32x32

# Move the input to the appropriate device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
input_image = input_image.to(device)

# Forward pass
output = model(input_image)

# Get the predicted class
_, predicted_class = torch.max(output, 1)
print(f"Predicted class: {predicted_class.item()}")

# ===== cell separator =====

# Save the model
torch.save(model.state_dict(), 'model.pth')