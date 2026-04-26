import os
import pickle

class DiskCache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, key)

    def _load_from_disk(self, key):
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None

    def _save_to_disk(self, key, obj):
        cache_path = self._get_cache_path(key)
        with open(cache_path, 'wb') as f:
            pickle.dump(obj, f)

    def get(self, key):
        obj = self._load_from_disk(key)
        if obj is None:
            obj = self._load_from_disk(key)
            if obj is None:
                raise KeyError(f"Key '{key}' not found in cache.")
        return obj

    def set(self, key, obj):
        self._save_to_disk(key, obj)

# Example usage
cache = DiskCache('my_cache')

# Set an object in the cache
cache.set('my_key', {'name': 'John', 'age': 30})

# Get the object from the cache
obj = cache.get('my_key')
print(obj)  # Output: {'name': 'John', 'age': 30}