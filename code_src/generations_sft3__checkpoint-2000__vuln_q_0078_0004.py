import tensorflow as tf
import os
import sys
from typing import Optional

def create_session_with_config(
    gpu_memory_limit_mb: int = 2048,
    log_device_placement: bool = False,
    allow_growth: bool = True
) -> Optional[tf.compat.v1.Session]:
    """
    Creates a TensorFlow session with secure configuration.
    
    Args:
        gpu_memory_limit_mb: Maximum GPU memory allocation limit (default: 2048MB)
        log_device_placement: Whether to log device placement (default: False)
        allow_growth: Whether to enable GPU memory growth (default: True)
    
    Returns:
        tf.compat.v1.Session object or None if creation fails
    """
    try:
        # Create session with secure configuration
        config = tf.compat.v1.ConfigProto(
            gpu_options=tf.compat.v1.GPUOptions(
                per_process_gpu_memory_fraction=gpu_memory_limit_mb / 1024
            ),
            log_device_placement=log_device_placement,
            allow_soft_placement=True,
            inter_op_memory_pool=tf.compat.v1.TF_MEMORY_POOL策略,
            intra_op_memory_pool=tf.compat.v1.TF_MEMORY_POOL策略
        )
        
        # Set allow_growth if requested
        if allow_growth:
            config.gpu_options.allow_growth = True
            
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
        session: tf.compat.v1.Session object to close
    """
    if session is not None:
        try:
            session.close()
        except Exception as e:
            print(f"Error closing TensorFlow session: {str(e)}", file=sys.stderr)