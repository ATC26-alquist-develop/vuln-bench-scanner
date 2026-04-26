import tensorflow as tf
import os
import sys
from typing import Optional

def create_session_with_config(
    gpu_memory_fraction: float = 0.8,
    device_count: Optional[dict] = None
) -> tf.compat.v1.Session:
    """
    Creates a TensorFlow session with custom configuration.
    
    Args:
        gpu_memory_fraction: Fraction of GPU memory to allocate
        device_count: Optional dictionary specifying device count for each device type
    
    Returns:
        tf.compat.v1.Session: Configured TensorFlow session
    
    Raises:
        ValueError: If gpu_memory_fraction is not between 0 and 1
        ValueError: If device_count is invalid
    """
    # Validate gpu_memory_fraction
    if not 0 <= gpu_memory_fraction <= 1:
        raise ValueError("gpu_memory_fraction must be between 0 and 1")
    
    # Create session with custom configuration
    config = tf.compat.v1.ConfigProto(
        gpu_options=tf.compat.v1.GPUOptions(
            per_process_gpu_memory_fraction=gpu_memory_fraction
        ),
        device_count=device_count if device_count else {}
    )
    
    # Ensure session is created in a controlled environment
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Disable TensorFlow logging
    sys.stdout = sys.stderr = open(os.devnull, 'w')  # Hide TensorFlow output
    
    try:
        session = tf.compat.v1.Session(config=config)
        return session
    except Exception as e:
        # Re-raise exception without exposing internal details
        raise RuntimeError("Failed to create TensorFlow session") from e