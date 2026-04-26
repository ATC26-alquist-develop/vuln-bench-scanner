import torch

# Assuming you have a trained model called 'my_model'

# Load the trained model

model = torch.load('my_model.pth')

# Set the model to evaluation mode

model.eval()


# Prepare your input data

# For example, let's say we have a single image tensor

input_data = torch.randn(1, 3, 224, 224)  # Batch size of 1, 3 color channels, 224x224 pixels


# Run the model on the input data

with torch.no_grad():  # No need to track gradients for inference

    output = model(input_data)


# Process the output

# For example, if your model outputs class probabilities, you can get the predicted class

predicted_class = output.argmax(dim=1)

print(f'Predicted class: {predicted_class.item()}')