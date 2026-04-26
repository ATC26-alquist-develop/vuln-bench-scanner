import tensorflow as tf
from tensorflow.python import pywrap_tensorflow
import os

def load_graph_from_file(graph_file_path):
    """
    Securely load a TensorFlow graph from a file using the older session-based API.
    
    Args:
        graph_file_path (str): Path to the TensorFlow graph file.
    
    Returns:
        tf.Graph: Loaded TensorFlow graph.
    """
    # Validate file path
    if not os.path.exists(graph_file_path):
        raise FileNotFoundError(f"Graph file not found: {graph_file_path}")
    
    # Check file extension
    if not graph_file_path.lower().endswith(('.pb', '.pbtxt')):
        raise ValueError("Invalid file format. Only .pb and .pbtxt files are supported.")
    
    # Load graph using older API
    graph_def = pywrap_tensorflow.NewCheckpointReader(graph_file_path)
    graph = tf.Graph()
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')
    
    return graph

def get_tensor_by_name(graph, tensor_name):
    """
    Securely retrieve a tensor from the loaded graph using its name.
    
    Args:
        graph (tf.Graph): Loaded TensorFlow graph.
        tensor_name (str): Name of the tensor to retrieve.
    
    Returns:
        tf.Tensor: Retrieved tensor.
    """
    if not isinstance(tensor_name, str):
        raise TypeError("Tensor name must be a string")
    
    tensor = graph.get_tensor_by_name(tensor_name)
    if tensor is None:
        raise ValueError(f"Tensor with name {tensor_name} not found in the graph")
    
    return tensor