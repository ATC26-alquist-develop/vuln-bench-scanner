import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim

# Step 1: Load the pre-trained model
model = torchvision.models.resnet18(pretrained=True)

# Step 2: Define the model
# Since we are using a pre-trained model, we don't need to define the model architecture.
# We will use the model as it is.

# Step 3: Load the dataset
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# Step 4: Load the pre-trained weights
# Since the model is already pre-trained, we don't need to load any weights.

# Step 5: Make predictions
# We will use the model to predict the class of a sample from the test set.
# Let's take the first sample from the test set.

dataiter = iter(testloader)
images, labels = dataiter.next()

# Move tensors to the GPU if available
if torch.cuda.is_available():
    images, labels = images.cuda(), labels.cuda()

# Forward pass
outputs = model(images)

# Step 6: Make predictions
_, predicted = torch.max(outputs, 1)

print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(4)))
print('Actual:    ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))