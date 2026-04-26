import tensorflow as tf
import os
import sys
from typing import Optional

def create_session(config: Optional[tf.ConfigProto] = None) -> tf.compat.v1.Session:
    """
    Creates a TensorFlow session with security considerations.
    
    Args:
        config: Optional configuration for the session
        
    Returns:
        tf.compat.v1.Session: A TensorFlow session
        
    Raises:
        RuntimeError: If TensorFlow is not properly initialized
    """
    try:
        # Verify TensorFlow version compatibility
        if not tf.__version__.startswith('2.'):
            raise RuntimeError("This function requires TensorFlow 2.x")
            
        # Create session with security considerations
        session = tf.compat.v1.Session(config=config)
        return session
        
    except Exception as e:
        # Log error securely (implement proper logging)
        print(f"Error creating TensorFlow session: {str(e)}", file=sys.stderr)
        raise

def run_session(session: tf.compat.v1.Session, 
                fetches: Optional[tf.TensorArray] = None,
                feed_dict: Optional[dict] = None) -> Optional[tf.TensorArray]:
    """
    Runs TensorFlow operations in the session with security measures.
    
    Args:
        session: TensorFlow session to run operations in
        fetches: Tensors to fetch from the session
        feed_dict: Feed dictionary for feeding values to placeholders
        
    Returns:
        Optional[tf.TensorArray]: TensorArray containing the results
        
    Raises:
        RuntimeError: If session operations fail
    """
    try:
        # Validate inputs
        if fetches is not None and not isinstance(fetches, (list, tuple)):
            raise TypeError("fetches must be a list or tuple")
        if feed_dict is not None and not isinstance(feed_dict, dict):
            raise TypeError("feed_dict must be a dictionary")
            
        # Run session with proper error handling
        results = session.run(fetches=fetches, feed_dict=feed_dict)
        return tf.TensorArray(results)
        
    except Exception as e:
        # Log error securely (implement proper logging)
        print(f"Error running TensorFlow session: {str(e)}", file=sys.stderr)
        raise

def close_session(session: tf.compat.v1.Session) -> None:
    """
    Safely closes a TensorFlow session.
    
    Args:
        session: TensorFlow session to close
        
    Raises:
        RuntimeError: If session is not properly closed
    """
    try:
        if not isinstance(session, tf.compat.v1.Session):
            raise TypeError("Invalid session type")
            
        session.close()
    except Exception as e:
        # Log error securely (implement proper logging)
        print(f"Error closing TensorFlow session: {str(e)}", file=sys.stderr)
        raise