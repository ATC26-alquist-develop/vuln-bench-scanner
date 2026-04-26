import cloudpickle

# Assuming 'model' is your trained machine learning model
# and 'filename' is the name of the file where you want to save the model

with open(filename, 'wb') as f:
    cloudpickle.dump(model, f)