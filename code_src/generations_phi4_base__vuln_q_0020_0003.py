import torch
import torchvision.models as models

# Load the pre-trained model
model = models.resnet18(pretrained=True)

# Set the model to evaluation mode
model.eval()

# Define the input tensor
input_tensor = torch.randn(1, 3, 224, 224)

# Perform the prediction
output = model(input_tensor)

# Print the output
print(output)