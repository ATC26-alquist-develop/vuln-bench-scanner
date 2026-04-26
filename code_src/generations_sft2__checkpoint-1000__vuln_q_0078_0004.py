import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import resource_variable_ops
import tensorflow.compat.v1 as tf_compat

def use_session_based_api():
    # Disable eager execution to force TensorFlow to use sessions
    tf_compat.v1.disable_eager_execution()
    
    # Create a TensorFlow graph
    graph = tf_compat.Graph()
    
    # Create a session with the graph
    with graph.as_default():
        # Create a session
        session = tf_compat.Session(graph=graph)
        
        # Define operations
        a = tf_compat.constant(5.0)
        b = tf_compat.constant(3.0)
        c = tf_compat.add(a, b)
        
        # Run the operation
        result = session.run(c)
        
        print(f"Result of addition: {result}")
        
        # Close the session
        session.close()

if __name__ == "__main__":
    use_session_based_api()