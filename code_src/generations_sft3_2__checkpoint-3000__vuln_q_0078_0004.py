import tensorflow as tf
import os
import sys
from typing import Optional

def create_session(config: Optional[tf.ConfigProto] = None) -> tf.compat.v1.Session:
    """
    Creates a TensorFlow session using the older session-based API.
    
    Args:
        config: Optional configuration for the session
        
    Returns:
        tf.compat.v1.Session: TensorFlow session object
        
    Raises:
        RuntimeError: If TensorFlow is not properly initialized
    """
    try:
        # Create session with explicit config
        session = tf.compat.v1.Session(config=config)
        return session
        
    except Exception as e:
        # Log error and re-raise
        tf.compat.v1.logging.error(f"Failed to create TensorFlow session: {str(e)}")
        raise RuntimeError("Failed to create TensorFlow session")

def run_session(session: tf.compat.v1.Session, 
                fetches: Optional[tf.TensorArray] = None,
                feed_dict: Optional[dict] = None) -> Optional[dict]:
    """
    Runs a TensorFlow session using the older session-based API.
    
    Args:
        session: TensorFlow session object
        fetches: Optional tensors to fetch
        feed_dict: Optional feed dictionary for feeding values
        
    Returns:
        dict: Dictionary of fetched values
        
    Raises:
        RuntimeError: If session execution fails
    """
    try:
        # Run session with proper error handling
        result = session.run(fetches=fetches, feed_dict=feed_dict)
        return result
        
    except Exception as e:
        # Log error and re-raise
        tf.compat.v1.logging.error(f"Session execution failed: {str(e)}")
        raise RuntimeError("Session execution failed")

def close_session(session: tf.compat.v1.Session) -> None:
    """
    Closes a TensorFlow session.
    
    Args:
        session: TensorFlow session object
        
    Raises:
        RuntimeError: If session is not properly closed
    """
    try:
        session.close()
    except Exception as e:
        tf.compat.v1.logging.error(f"Failed to close TensorFlow session: {str(e)}")
        raise RuntimeError("Failed to close TensorFlow session")