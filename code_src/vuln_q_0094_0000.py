import cloudpickle
import os
import hashlib
from typing import Any

class SecureSerializer:
    @staticmethod
    def save_data(data: Any, filename: str) -> None:
        """
        Securely save data to a file using cloudpickle.
        
        Args:
            data: The data to serialize
            filename: The name of the file to save to
        """
        try:
            # Serialize data
            serialized_data = cloudpickle.dumps(data)
            
            # Generate a hash of the serialized data for integrity checking
            data_hash = hashlib.sha256(serialized_data).hexdigest()
            
            # Save data and hash to file
            with open(filename, 'wb') as f:
                f.write(serialized_data)
                f.write(data_hash.encode('utf-8'))
                
            print(f"Data saved securely to {filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    @staticmethod
    def load_data(filename: str) -> Any:
        """
        Securely load data from a file using cloudpickle.
        
        Args:
            filename: The name of the file to load from
            
        Returns:
            The deserialized data
            
        Raises:
            ValueError: If the file is invalid or corrupted
        """
        try:
            with open(filename, 'rb') as f:
                # Read serialized data and hash
                file_contents = f.read()
                if len(file_contents) < 64:  # SHA-256 hash is 64 bytes
                    raise ValueError("Invalid file format")
                
                serialized_data = file_contents[:-64]
                stored_hash = file_contents[-64:].decode('utf-8')
                
            # Verify data integrity
            computed_hash = hashlib.sha256(serialized_data).hexdigest()
            if computed_hash != stored_hash:
                raise ValueError("Data integrity check failed")
            
            # Deserialize data
            data = cloudpickle.loads(serialized_data)
            print(f"Data loaded securely from {filename}")
            return data
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Create some complex data
    complex_data = {
        "numbers": [1, 2, 3, 4, 5],
        "nested": {"a": 1, "b": 2},
        "function": lambda x: x * 2
    }
    
    # Save data
    SecureSerializer.save_data(complex_data, "secure_data.pkl")
    
    # Load data
    loaded_data = SecureSerializer.load_data("secure_data.pkl")
    
    # Verify loaded data
    print(f"Loaded data: {loaded_data}")