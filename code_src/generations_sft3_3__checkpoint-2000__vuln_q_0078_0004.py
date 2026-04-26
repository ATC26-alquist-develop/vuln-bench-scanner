import tensorflow as tf
import os
import sys
from typing import Optional

def create_session_with_config(
    gpu_memory_limit_mb: int = 2048,
    log_device_placement: bool = False,
    allow_soft_placement: bool = True
) -> Optional[tf.compat.v1.Session]:
    """
    Creates a TensorFlow session with custom configuration.
    
    Args:
        gpu_memory_limit_mb: Maximum GPU memory allocation in MB
        log_device_placement: Whether to log device placement
        allow_soft_placement: Whether to allow soft placement of operations
    
    Returns:
        tf.compat.v1.Session or None if creation fails
    """
    try:
        # Create session with custom configuration
        config = tf.compat.v1.ConfigProto(
            gpu_options=tf.compat.v1.GPUOptions(
                per_process_gpu_memory_fraction=gpu_memory_limit_mb / 1024
            ),
            log_device_placement=log_device_placement,
            allow_soft_placement=allow_soft_placement
        )
        
        # Create session
        session = tf.compat.v1.Session(config=config)
        return session
        
    except Exception as e:
        print(f"Error creating TensorFlow session: {str(e)}", file=sys.stderr)
        return None

def cleanup_session(session: Optional[tf.compat.v1.Session]) -> None:
    """
    Safely close a TensorFlow session.
    
    Args:
        session: TensorFlow session to close
    """
    if session is not None:
        try:
            session.close()
        except Exception as e:
            print(f"Error closing TensorFlow session: {str(e)}", file=sys.stderr)