import tensorflow as tf
from tensorflow.compat.v1 import Session, run
from tensorflow.compat.v1 import graph, Session as TFSession

def safe_session_run(graph, feed_dict=None, fetches=None):
    """
    Safely run a TensorFlow graph using the session-based API.
    
    Args:
        graph: A TensorFlow graph object
        feed_dict: Optional dictionary of feed values
        fetches: Optional list of tensors to fetch
    
    Returns:
        A tuple of fetched values if successful, None otherwise
    """
    try:
        # Create a new session with default graph
        with TFSession(graph=graph) as session:
            # Run the graph with optional feed and fetches
            results = session.run(fetches=fetches, feed_dict=feed_dict)
            return results
    except Exception as e:
        print(f"Error during session run: {e}")
        return None

# Example usage:
# graph = tf.Graph()
# with graph.as_default():
#     # Define your model here
#     ...
#     results = safe_session_run(graph, feed_dict={...}, fetches=[...])