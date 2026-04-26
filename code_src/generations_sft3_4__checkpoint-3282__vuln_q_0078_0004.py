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
        # Create session with explicit graph
        session = tf.compat.v1.Session(config=config)
        return session
        
    except Exception as e:
        # Log error and re-raise
        tf.compat.v1.logging.error(f"Failed to create TensorFlow session: {str(e)}")
        raise RuntimeError("Failed to create TensorFlow session") from e

def run_session(session: tf.compat.v1.Session, 
                fetches: Optional[tf.TensorArray] = None,
                feed_dict: Optional[dict] = None) -> Optional[tf.TensorArray]:
    """
    Runs a TensorFlow session using the older session-based API.
    
    Args:
        session: TensorFlow session object
        fetches: Tensors to fetch
        feed_dict: Feed dictionary for feeding values to placeholders
        
    Returns:
        Optional[tf.TensorArray]: TensorArray containing the results
        
    Raises:
        RuntimeError: If session execution fails
    """
    try:
        # Run session with proper error handling
        results = session.run(fetches=fetches, feed_dict=feed_dict)
        return tf.TensorArray(results)
        
    except Exception as e:
        tf.compat.v1.logging.error(f"Session execution failed: {str(e)}")
        raise RuntimeError("Session execution failed") from e

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
        raise RuntimeError("Failed to close TensorFlow session") from e

# Example usage
if __name__ == "__main__":
    try:
        # Create session with explicit config
        config = tf.ConfigProto(intra_op_parallelism_threads=4,
                               inter_op_parallelism_threads=4)
        session = create_session(config=config)
        
        # Run session
        fetches = [tf.constant(1.0), tf.constant(2.0)]
        results = run_session(session, fetches=fetches)
        
        # Close session
        close_session(session)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)