import pickle
import hmac
import hashlib
import os

def secure_serialize(data, secret_key):
    """
    Securely serialize a Python object using HMAC for integrity verification.
    
    Args:
        data: The Python object to serialize
        secret_key: A secret key for HMAC generation
    
    Returns:
        A tuple containing the serialized data and its HMAC
    """
    serialized_data = pickle.dumps(data)
    hmac_obj = hmac.new(secret_key, serialized_data, hashlib.sha256)
    return serialized_data, hmac_obj.digest()

def secure_deserialize(serialized_data, hmac_digest, secret_key):
    """
    Securely deserialize a Python object and verify its integrity.
    
    Args:
        serialized_data: The serialized Python object
        hmac_digest: The HMAC digest to verify against
        secret_key: The same secret key used for HMAC generation
    
    Returns:
        The deserialized Python object
    
    Raises:
        ValueError: If the HMAC verification fails
        pickle.UnpicklingError: If the data is not properly serialized
    """
    hmac_obj = hmac.new(secret_key, serialized_data, hashlib.sha256)
    if hmac.compare_digest(hmac_obj.digest(), hmac_digest):
        return pickle.loads(serialized_data)
    else:
        raise ValueError("Data integrity check failed")