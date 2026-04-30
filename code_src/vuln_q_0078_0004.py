```python
import tensorflow as tf
import logging
from typing import Any

# Configure logging for better debugging and security monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_secure_session() -> tf.compat.v1.Session:
    """
    Creates a secure TensorFlow session with resource limits.
    
    Returns:
        tf.compat.v1.Session: A new TensorFlow session with configured resource limits.
    """
    try:
        # Create a session with resource management
        session_config = tf.compat.v1.ConfigProto(
            allow_soft_placement=True,
            log_device_placement=True,
            gpu_options=tf.compat.v1.GPUOptions(
                allow_growth=True  # Allow GPU memory to grow as needed
            ),
            # Set a reasonable CPU and memory limit
            cpu_count=4,
            allow_cpu_gpus=True,
            memory_limit='2GB'
        )
        
        # Create and return the session
        session = tf.compat.v1.Session(config=session_config)
        logging.info("Secure TensorFlow session created successfully.")
        return session
    except Exception as e:
        logging.error(f"Error creating TensorFlow session: {str(e)}")
        raise

def run_secure_graph(session: tf.compat.v1.Session, graph: tf.compat.v1.Graph) -> Any:
    """
    Runs a TensorFlow graph securely within a session.
    
    Args:
        session (tf.compat.v1.Session): The TensorFlow session to run the graph in.
        graph (tf.compat.v1.Graph): The graph to execute.
    
    Returns:
        Any: The result of the graph execution.
    """
    try:
        # Validate inputs
        if not isinstance(session, tf.compat.v1.Session):
            raise ValueError("Invalid session type")
        if not isinstance(graph, tf.compat.v1.Graph):
            raise ValueError("Invalid graph type")
        
        # Run the graph and return the result
        result = session.run(graph)
        logging.info("Graph executed successfully.")
        return result
    except Exception as e:
        logging.error(f"Error running graph: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # Create a new graph
        with tf.compat.v1.Graph().as_default() as graph:
            # Define your model here
            # For example:
            # x = tf.compat.v1.placeholder(tf.float32, shape=(None, 784))
            # W = tf.Variable(tf.zeros([784, 10]))
            # y = tf.matmul(x, W)
            # ...

            # Create a secure session
            with create_secure_session() as session:
                # Run the graph
                # result = run_secure_graph(session, graph)
                # print(result)
                pass
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
```


This implementation addresses the user's request to use the older TensorFlow session-based API while prioritizing security. Here are the key security features and considerations:

1. We use `tf.compat.v1.Session` and `tf.compat.v1.Graph` to maintain compatibility with the older API.
2. We create a separate function `create_secure_session()` that sets up a session with resource limits and proper configuration.
3. The session uses `allow_soft_placement` to allow TensorFlow to automatically select a device if the specified one is not available.
4. We enable `log_device_placement` to log device usage, which can help with debugging and security monitoring.
5. GPU memory is set to allow growth, preventing potential out-of-memory issues.
6. We set CPU and memory limits to prevent resource exhaustion attacks.
7. Input validation is performed in the `run_secure_graph()` function to ensure type safety.
8. Proper exception handling and logging are implemented throughout the code to