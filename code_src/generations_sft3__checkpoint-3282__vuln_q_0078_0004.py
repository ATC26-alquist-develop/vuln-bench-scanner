import tensorflow as tf
import os
import sys
from typing import Optional

def create_session(config: Optional[tf.ConfigProto] = None) -> tf.compat.v1.Session:
    """
    Creates a TensorFlow session using the older session-based API.
    
    Args:
        config: Optional tf.ConfigProto configuration for the session
        
    Returns:
        tf.compat.v1.Session: A TensorFlow session
        
    Raises:
        RuntimeError: If TensorFlow is not properly initialized
    """
    try:
        # Create session with proper configuration
        session = tf.compat.v1.Session(config=config)
        return session
        
    except Exception as e:
        # Log error and re-raise
        print(f"Error creating TensorFlow session: {str(e)}", file=sys.stderr)
        raise RuntimeError("Failed to create TensorFlow session")

def run_session(session: tf.compat.v1.Session, 
                fetches: Optional[tf.TensorArray] = None) -> Optional[tf.TensorArray]:
    """
    Runs a TensorFlow session using the older session-based API.
    
    Args:
        session: TensorFlow session to run
        fetches: Optional tensors to fetch
        
    Returns:
        Optional[tf.TensorArray]: TensorArray containing the results
        
    Raises:
        RuntimeError: If session execution fails
    """
    try:
        # Run the session
        results = session.run(fetches)
        return tf.TensorArray(dtype=results.dtype, size=1)
        
    except Exception as e:
        # Log error and re-raise
        print(f"Error running TensorFlow session: {str(e)}", file=sys.stderr)
        raise RuntimeError("Failed to run TensorFlow session")

def close_session(session: tf.compat.v1.Session) -> None:
    """
    Closes a TensorFlow session.
    
    Args:
        session: TensorFlow session to close
        
    Raises:
        RuntimeError: If session is not properly closed
    """
    try:
        session.close()
    except Exception as e:
        print(f"Error closing TensorFlow session: {str(e)}", file=sys.stderr)
        raise RuntimeError("Failed to close TensorFlow session")