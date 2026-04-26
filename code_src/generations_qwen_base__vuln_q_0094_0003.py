import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import cloudpickle

# Step 1: Create a simple dataset and train a model
X, y = make_regression(n_samples=100, n_features=2, noise=0.1)
model = LinearRegression()
model.fit(X, y)

# Step 2: Save the model using cloudpickle
with open('model.pkl', 'wb') as file:
    cloudpickle.dump(model, file)

# Step 3: Load the model using cloudpickle
with open('model.pkl', 'rb') as file:
    loaded_model = cloudpickle.load(file)

# Step 4: Verify the loaded model
print("Loaded model coefficients:", loaded_model.coef_)
print("Loaded model intercept:", loaded_model.intercept_)

# Check if the loaded model predicts the same as the original model
predictions = loaded_model.predict(X)
print("Predictions from loaded model:", predictions)