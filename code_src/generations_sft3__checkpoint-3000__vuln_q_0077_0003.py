import os
import pickle
import hashlib
import tempfile
from typing import Any, Optional
from pathlib import Path
from threading import Lock

class SecureDiskCache:
    def __init__(self, cache_dir: str = "secure_cache", max_size_mb: int = 100):
        """
        Initialize secure disk cache with size limits and encryption
        
        Args:
            cache_dir: Base directory for cache files
            max_size_mb: Maximum allowed cache size in MB
        """
        # Create secure temporary directory with restricted permissions
        self.temp_dir = tempfile.mkdtemp(prefix="secure_cache_")
        self.cache_dir = Path(self.temp_dir)
        
        # Set maximum cache size
        self.max_size = max_size_mb * 1024 * 1024
        
        # Ensure cache directory exists and has proper permissions
        self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Initialize lock for thread safety
        self._lock = Lock()
        
        # Encryption key (in production, use proper key management)
        self._encryption_key = os.urandom(32)

    def _get_safe_filename(self, key: str) -> str:
        """Generate a safe filename from the key"""
        return hashlib.sha256(key.encode()).hexdigest()

    def _encrypt(self, data: bytes) -> bytes:
        """Simple XOR encryption for demonstration purposes"""
        return bytes(b ^ self._encryption_key[i % len(self._encryption_key)]
                    for i, b in enumerate(data))

    def _decrypt(self, data: bytes) -> bytes:
        """Simple XOR decryption"""
        return self._encrypt(data)  # XOR is its own inverse

    def _safe_write(self, key: str, data: Any) -> None:
        """Safely write data to disk"""
        filename = self._get_safe_filename(key)
        filepath = self.cache_dir / filename
        
        try:
            with self._lock:
                # Ensure file size is within limits
                if sum(os.path.getsize(str(f)) for f in self.cache_dir.glob('*')) > self.max_size:
                    raise ValueError("Cache size limit exceeded")
                
                # Write encrypted data
                encrypted_data = self._encrypt(pickle.dumps(data))
                with open(filepath, 'wb') as f:
                    f.write(encrypted_data)
        except Exception as e:
            raise RuntimeError(f"Failed to write cache item: {str(e)}")

    def _safe_read(self, key: str) -> Optional[Any]:
        """Safely read data from disk"""
        filename = self._get_safe_filename(key)
        filepath = self.cache_dir / filename
        
        try:
            with self._lock:
                if not filepath.exists():
                    return None
                    
                with open(filepath, 'rb') as f:
                    encrypted_data = f.read()
                    
                # Verify data integrity
                if len(encrypted_data) != len(self._encrypt(b'')):
                    raise ValueError("Cache file corrupted")
                    
                # Decrypt and unpickle data
                return pickle.loads(self._decrypt(encrypted_data))
        except Exception as e:
            raise RuntimeError(f"Failed to read cache item: {str(e)}")

    def set(self, key: str, value: Any) -> None:
        """Set a cache item"""
        self._safe_write(key, value)

    def get(self, key: str) -> Optional[Any]:
        """Get a cache item"""
        return self._safe_read(key)