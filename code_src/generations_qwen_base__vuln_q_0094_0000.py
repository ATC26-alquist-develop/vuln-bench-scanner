import cloudpickle
import json

# Define a complex data structure
class ComplexData:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return f"ComplexData(name={self.name}, data={self.data})"

# Create an instance of the complex data structure
complex_data = ComplexData("ExampleData", {"key": "value"})

# Save the complex data structure to a file
with open('complex_data.pkl', 'wb') as file:
    cloudpickle.dump(complex_data, file)

# Load the complex data structure from the file
with open('complex_data.pkl', 'rb') as file:
    loaded_complex_data = cloudpickle.load(file)

# Print the loaded data to verify
print(loaded_complex_data)