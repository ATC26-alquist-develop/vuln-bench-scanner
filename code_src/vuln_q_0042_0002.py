```python
import multiprocessing
from typing import Any
from functools import partial

def create_secure_shared_data(data: Any) -> multiprocessing.managers.BaseManager:
    """
    Creates a secure shared data manager with type checking and validation.
    
    Args:
        data: Initial data to share between processes
        
    Returns:
        A BaseManager instance for secure inter-process communication
    """
    # Validate input data
    if not data:
        raise ValueError("Data cannot be None or empty")
        
    # Create a manager with only necessary methods
    manager = multiprocessing.managers.BaseManager(
        allow_none=False,  # Prevent None references
        authname='SecureSharedData',
        authkey=b'securekey123',  # Use a strong key in production
        authgroup='shared'
    )
    
    # Store data in a private attribute
    manager._data = data
    
    # Add a secure get method
    def get_data() -> Any:
        return manager._data
    
    manager.get_data = get_data.__get__(manager)
    
    return manager

def main():
    # Example usage
    try:
        # Create and start child process
        with multiprocessing.Pool(1) as pool:
            # Create shared data manager
            manager = create_secure_shared_data([1, 2, 3])
            
            # Get data in child process
            result = pool.apply_async(get_data)
            print(f"Child process received: {result.get()}")
            
            # Get data in parent process
            print(f"Parent process received: {manager.get_data()}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
```