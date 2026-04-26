import cloudpickle
import os

def save_data(data, filename):
    try:
        with open(filename, 'wb') as file:
            cloudpickle.dump(data, file)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as file:
                data = cloudpickle.load(file)
            print(f"Data loaded from {filename}")
            return data
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
    else:
        print(f"The file {filename} does not exist.")
        return None

# Example usage:
data_to_save = {'key': 'value', 'list': [1, 2, 3]}
save_data(data_to_save, 'data.pkl')

loaded_data = load_data('data.pkl')
print(loaded_data)