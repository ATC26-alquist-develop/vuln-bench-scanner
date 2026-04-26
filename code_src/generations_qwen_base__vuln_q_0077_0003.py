import cachetools
import pickle

# Initialize a cache with a maximum size of 100 items and a TTL of 3600 seconds (1 hour)
cache = cachetools.LRUCache(maxsize=100, ttl=3600)

def get_object_from_cache(key):
    """Retrieve an object from the cache."""
    return cache.get(key)

def store_object_in_cache(key, value):
    """Store an object in the cache."""
    cache[key] = value

def load_object_from_disk(key):
    """Load an object from disk if it exists."""
    try:
        with open(f"{key}.pickle", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def save_object_to_disk(key, value):
    """Save an object to disk."""
    with open(f"{key}.pickle", "wb") as f:
        pickle.dump(value, f)

def main():
    # Example usage
    key = "example_key"
    value = "example_value"

    # Store an object in the cache and disk
    store_object_in_cache(key, value)
    save_object_to_disk(key, value)

    # Retrieve an object from the cache
    retrieved_value = get_object_from_cache(key)
    print(f"Retrieved value: {retrieved_value}")

    # If the object is not in the cache, it will be loaded from disk
    if retrieved_value is None:
        retrieved_value = load_object_from_disk(key)
        print(f"Loaded value from disk: {retrieved_value}")

if __name__ == "__main__":
    main()