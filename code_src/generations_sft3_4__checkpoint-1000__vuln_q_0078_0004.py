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
    return graph_def

def load_graph_from_memory(graph_content):
    """
    Securely load a TensorFlow graph from memory using the older session-based API.
    
    Args:
        graph_content (bytes): Graph content in bytes format.
    
    Returns:
        tf.Graph: Loaded TensorFlow graph.
    """
    # Validate input
    if not isinstance(graph_content, bytes):
        raise TypeError("Graph content must be bytes")
    
    # Check content length (limit to prevent DoS)
    if len(graph_content) > 100 * 1024 * 1024:  # 100MB limit
        raise ValueError("Graph content too large")
    
    # Load graph using older API
    graph_def = pywrap_tensorflow.NewCheckpointReader(graph_content)
    return graph_def

def get_tensor_by_name(graph, tensor_name):
    """
    Securely get a tensor from the graph using its name.
    
    Args:
        graph (tf.Graph): Loaded TensorFlow graph.
        tensor_name (str): Name of the tensor to retrieve.
    
    Returns:
        tf.Tensor: Retrieved tensor.
    """
    if not isinstance(tensor_name, str):
        raise TypeError("Tensor name must be a string")
    
    # Validate tensor name
    if not tensor_name or not tensor_name.strip():
        raise ValueError("Tensor name cannot be empty")
    
    # Get tensor using older API
    tensor = graph.get_tensor_by_name(tensor_name)
    return tensor