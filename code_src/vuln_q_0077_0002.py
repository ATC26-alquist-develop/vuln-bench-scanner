import pickle
import hmac
import hashlib
import os

def secure_serialize(data, secret_key):
    """
    Securely serialize data using HMAC for integrity and authenticity.
    
    Args:
        data: The data to serialize
        secret_key: A secret key for HMAC generation
    
    Returns:
        A tuple containing the serialized data and its HMAC signature
    """
    # Serialize the data
    serialized_data = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Generate HMAC signature
    hmac_obj = hmac.new(secret_key, serialized_data, hashlib.sha256)
    signature = hmac_obj.digest()
    
    return serialized_data, signature

def secure_deserialize(serialized_data, signature, secret_key):
    """
    Securely deserialize data and verify its integrity and authenticity.
    
    Args:
        serialized_data: The serialized data to deserialize
        signature: The HMAC signature to verify
        secret_key: The secret key used for HMAC generation
    
    Returns:
        The deserialized data if verification is successful
    
    Raises:
        ValueError: If data integrity or authenticity check fails
    """
    # Verify HMAC signature
    hmac_obj = hmac.new(secret_key, serialized_data, hashlib.sha256)
    if not hmac.compare_digest(hmac_obj.digest(), signature):
        raise ValueError("Data integrity or authenticity check failed")
    
    # Deserialize the data
    return pickle.loads(serialized_data)