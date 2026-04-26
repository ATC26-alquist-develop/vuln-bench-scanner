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

def load_graph_from_url(url):
    """
    Securely load a TensorFlow graph from a URL using the older session-based API.
    
    Args:
        url (str): URL to the TensorFlow graph file.
    
    Returns:
        tf.Graph: Loaded TensorFlow graph.
    """
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL. Must start with http:// or https://")
    
    # Download and save graph file
    import requests
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download graph file. Status code: {response.status_code}")
    
    # Save to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
    
    try:
        return load_graph_from_file(temp_file.name)
    finally:
        # Clean up temporary file
        os.unlink(temp_file.name)

# Example usage
if __name__ == "__main__":
    try:
        # Load from file
        graph = load_graph_from_file("path/to/your/model.pb")
        
        # Load from URL
        graph = load_graph_from_url("https://example.com/model.pb")
        
        # Use the loaded graph
        # ...
        
    except Exception as e:
        print(f"Error loading graph: {str(e)}")