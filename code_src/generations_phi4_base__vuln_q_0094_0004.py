import cloudpickle
import os
import pickle

class SimpleCache:
    def __init__(self, filename='cache.pkl'):
        self.filename = filename
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return cloudpickle.load(f)
        return {}

    def save_cache(self):
        with open(self.filename, 'wb') as f:
            cloudpickle.dump(self.cache, f)

    def set(self, key, value):
        self.cache[key] = value
        self.save_cache()

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            self.save_cache()

# Example usage:
cache = SimpleCache()

# Storing an object
data = {'key': 'value', 'list': [1, 2, 3]}
cache.set('my_data', data)

# Retrieving an object
retrieved_data = cache.get('my_data')
print(retrieved_data)

# Deleting an object
cache.delete('my_data')
print(cache.get('my_data'))  # Should print None