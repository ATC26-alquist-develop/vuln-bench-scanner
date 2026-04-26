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
        RuntimeError: If TensorFlow is not properly installed or initialized
    """
    try:
        # Verify TensorFlow is properly installed
        if not hasattr(tf, 'version'):
            raise RuntimeError("TensorFlow is not properly installed")
            
        # Create session with proper configuration
        session = tf.compat.v1.Session(config=config)
        return session
        
    except Exception as e:
        # Log error and re-raise
        print(f"Error creating TensorFlow session: {str(e)}", file=sys.stderr)
        raise

def run_session(session: tf.compat.v1.Session, 
                fetches: Optional[tf.TensorArray] = None,
                feed_dict: Optional[dict] = None) -> Optional[tf.TensorArray]:
    """
    Runs a TensorFlow session using the older session-based API.
    
    Args:
        session: TensorFlow session object
        fetches: Optional tensors to fetch
        feed_dict: Optional feed dictionary for feeding values
        
    Returns:
        Optional[tf.TensorArray]: TensorArray containing the results
        
    Raises:
        RuntimeError: If session is invalid or operation fails
    """
    try:
        # Validate session
        if not isinstance(session, tf.compat.v1.Session):
            raise RuntimeError("Invalid session object")
            
        # Run session with proper error handling
        results = session.run(fetches=fetches, feed_dict=feed_dict)
        return tf.TensorArray(results)
        
    except Exception as e:
        # Log error and re-raise
        print(f"Error running TensorFlow session: {str(e)}", file=sys.stderr)
        raise

def close_session(session: tf.compat.v1.Session) -> None:
    """
    Closes a TensorFlow session.
    
    Args:
        session: TensorFlow session object
        
    Raises:
        RuntimeError: If session is invalid
    """
    try:
        if not isinstance(session, tf.compat.v1.Session):
            raise RuntimeError("Invalid session object")
            
        session.close()
    except Exception as e:
        print(f"Error closing TensorFlow session: {str(e)}", file=sys.stderr)
        raise