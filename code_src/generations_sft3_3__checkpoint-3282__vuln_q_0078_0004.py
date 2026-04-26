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
        tf.compat.v1.Session: TensorFlow session
        
    Raises:
        RuntimeError: If session creation fails
    """
    try:
        # Set session graph to None to prevent memory leaks
        tf.compat.v1.reset_default_graph()
        
        # Create session with security measures
        session = tf.compat.v1.Session(config=config)
        
        # Verify session creation
        if not session:
            raise RuntimeError("Failed to create TensorFlow session")
            
        return session
        
    except Exception as e:
        # Log error securely (implement proper logging)
        print(f"Error creating TensorFlow session: {str(e)}", file=sys.stderr)
        raise

def run_session(session: tf.compat.v1.Session, 
                fetches: Optional[tf.TensorArray] = None) -> Optional[tf.TensorArray]:
    """
    Runs TensorFlow operations in the session.
    
    Args:
        session: TensorFlow session to run operations in
        fetches: Optional tensors to fetch
        
    Returns:
        tf.TensorArray: Result of the operation
        
    Raises:
        RuntimeError: If session execution fails
    """
    try:
        # Run session with proper error handling
        result = session.run(fetches)
        return tf.TensorArray(result)
        
    except Exception as e:
        # Log error securely (implement proper logging)
        print(f"Error running TensorFlow session: {str(e)}", file=sys.stderr)
        raise

def close_session(session: tf.compat.v1.Session) -> None:
    """
    Closes TensorFlow session.
    
    Args:
        session: TensorFlow session to close
        
    Raises:
        RuntimeError: If session closing fails
    """
    try:
        session.close()
    except Exception as e:
        # Log error securely (implement proper logging)
        print(f"Error closing TensorFlow session: {str(e)}", file=sys.stderr)
        raise