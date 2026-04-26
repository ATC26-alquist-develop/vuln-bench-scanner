import msgpack

# Define a complex data structure
class ComplexData:
    def __init__(self, name, age, data):
        self.name = name
        self.age = age
        self.data = data

    def __repr__(self):
        return f"ComplexData(name={self.name}, age={self.age}, data={self.data})"

# Create an instance of the complex data structure
data = ComplexData("Alice", 30, {"key": "value"})

# Serialize the data
packed_data = msgpack.packb(data)

# Deserialize the data
unpacked_data = msgpack.unpackb(packed_data)

# Print the unpacked data
print(unpacked_data)

# ===== cell separator =====

import json

# Define a complex data structure
class ComplexData:
    def __init__(self, name, age, data):
        self.name = name
        self.age = age
        self.data = data

    def __repr__(self):
        return f"ComplexData(name={self.name}, age={self.age}, data={self.data})"

# Create an instance of the complex data structure
data = ComplexData("Alice", 30, {"key": "value"})

# Serialize the data
json_data = json.dumps(data.__dict__)

# Deserialize the data
unpacked_data = json.loads(json_data)

# Print the unpacked data
print(unpacked_data)