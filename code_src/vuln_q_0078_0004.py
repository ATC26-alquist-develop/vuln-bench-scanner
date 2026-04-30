import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import resource_variable_ops
import tensorflow.compat.v1 as tf_compat

def use_session_based_api():
    # Disable eager execution to force TensorFlow to use sessions
    tf_compat.v1.disable_eager_execution()
    
    # Create a TensorFlow graph
    graph = tf_compat.v1.Graph()
    with graph.as_default():
        # Define your model here
        # Example: a simple placeholder
        x = tf_compat.v1.placeholder(tf.float32, shape=(None, 10))
        
        # Define operations
        y = tf_compat.v1.matmul(x, tf_compat.v1.constant([[1, 2], [3, 4]]))
        
        # Initialize variables
        init_op = tf_compat.v1.global_variables_initializer()
    
    # Create a session
    with tf_compat.v1.Session(graph=graph) as sess:
        # Initialize variables
        sess.run(init_op)
        
        # Run operations
        result = sess.run(y, feed_dict={x: [[1, 2], [3, 4]]})
        
        return result

# Example usage
if __name__ == "__main__":
    result = use_session_based_api()
    print("Result:", result)