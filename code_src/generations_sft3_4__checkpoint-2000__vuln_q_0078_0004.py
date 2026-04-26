import tensorflow as tf
import os
import sys
from typing import Optional

def create_session_with_config(
    gpu_memory_limit_mb: Optional[int] = None,
    log_device_placement: bool = False,
    allow_growth: bool = False
) -> tf.compat.v1.Session:
    """
    Creates a TensorFlow session with custom configuration.
    
    Args:
        gpu_memory_limit_mb: Optional GPU memory limit in MB
        log_device_placement: Whether to log device placement
        allow_growth: Whether to allow GPU memory growth
    
    Returns:
        tf.compat.v1.Session: Configured TensorFlow session
    
    Raises:
        ValueError: If invalid parameters are provided
    """
    # Validate parameters
    if gpu_memory_limit_mb is not None and gpu_memory_limit_mb <= 0:
        raise ValueError("gpu_memory_limit_mb must be positive")
    
    if not isinstance(log_device_placement, bool):
        raise ValueError("log_device_placement must be boolean")
    
    if not isinstance(allow_growth, bool):
        raise ValueError("allow_growth must be boolean")

    # Create session configuration
    config = tf.compat.v1.ConfigProto(
        gpu_options=tf.compat.v1.GPUOptions(
            per_process_gpu_memory_fraction=0.8 if gpu_memory_limit_mb else None,
            allow_growth=allow_growth
        ),
        log_device_placement=log_device_placement
    )

    # Create session
    session = tf.compat.v1.Session(config=config)
    
    return session

def run_legacy_model(
    session: tf.compat.v1.Session,
    model_path: str,
    input_data: Optional[tf.Tensor] = None
) -> Optional[tf.Tensor]:
    """
    Runs a legacy TensorFlow model using the session.
    
    Args:
        session: TensorFlow session to use
        model_path: Path to the saved model
        input_data: Optional input tensor for the model
    
    Returns:
        Optional[tf.Tensor]: Output tensor from the model or None if error occurs
    """
    try:
        # Load the model
        with session.as_default():
            with tf.compat.v1.gfile.GFile(model_path, "rb") as model_file:
                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(model_file.read())
                tf.import_graph_def(graph_def, name="")
            
            # Get input and output nodes
            input_node = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
            output_node = tf.compat.v1.get_default_graph().get_tensor_by_name("output:0")
            
            # Run the model
            if input_data is None:
                output = session.run(output_node)
            else:
                output = session.run(output_node, feed_dict={input_node: input_data})
            
            return output
            
    except Exception as e:
        print(f"Error running model: {str(e)}", file=sys.stderr)
        return None