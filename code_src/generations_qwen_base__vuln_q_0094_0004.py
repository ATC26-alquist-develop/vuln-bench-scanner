import cloudpickle
import time

class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        # Check if the key exists in the cache
        if key in self.cache:
            # If the object is still in the cache, return it
            return self.cache[key]
        else:
            # If the object is not in the cache, return None
            return None

    def set(self, key, value):
        # Use cloudpickle to serialize the value
        serialized_value = cloudpickle.dumps(value)
        # Store the serialized value in the cache
        self.cache[key] = serialized_value

    def delete(self, key):
        # Check if the key exists in the cache
        if key in self.cache:
            # Remove the key from the cache
            del self.cache[key]

    def clear(self):
        # Clear the entire cache
        self.cache.clear()

    def get_with_timeout(self, key, timeout=300):
        # Check if the key exists in the cache
        if key in self.cache:
            # Check if the object is still valid within the timeout
            if time.time() - self.cache[key][1] < timeout:
                # If the object is still valid, return it
                return cloudpickle.loads(self.cache[key][0])
            else:
                # If the object is expired, remove it from the cache
                del self.cache[key]
        else:
            # If the key is not in the cache, return None
            return None

# Example usage
cache = SimpleCache()

# Set an object in the cache
cache.set('example_key', 'example_value')

# Get the object from the cache
print(cache.get_with_timeout('example_key'))  # Output: example_value

# Clear the cache
cache.clear()

# Try to get the object from the cache
print(cache.get_with_timeout('example_key'))  # Output: None