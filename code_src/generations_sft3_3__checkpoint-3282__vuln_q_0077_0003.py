```python
import os
import json
import hashlib
import tempfile
from typing import Any, Optional
from pathlib import Path
from threading import Lock
from datetime import datetime, timedelta

class SecureDiskCache:
    def __init__(self, 
                 max_size_bytes: int = 100_000_000,  # 100MB default
                 max_age_seconds: int = 3600,  # 1 hour default
                 cache_dir: str = "secure_cache"):
        """
        Initialize secure disk cache with safety limits and protections
        
        Args:
            max_size_bytes: Maximum total cache size
            max_age_seconds: Maximum age of cached items
            cache_dir: Base directory for cache files
        """
        self.max_size_bytes = max_size_bytes
        self.max_age_seconds = max_age_seconds
        self.cache_dir = Path(cache_dir).resolve()
        
        # Ensure cache directory exists and is secure
        self._ensure_secure_directory()
        
        # Thread-safe cache
        self._cache: dict[str, dict] = {}
        self._lock = Lock()
        
        # Track total cache size
        self._total_size = 0
        
    def _ensure_secure_directory(self) -> None:
        """Create cache directory with secure permissions"""
        try:
            self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise RuntimeError(f"Failed to create cache directory: {e}")
    
    def _get_cache_path(self, key: str) -> Path:
        """Generate secure file path for cache item"""
        # Use SHA256 for key hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.json"
    
    def _check_cache_limits(self) -> None:
        """Check if cache size limit is exceeded"""
        with self._lock:
            if self._total_size + 1 > self.max_size_bytes:
                raise RuntimeError("Cache size limit exceeded")
    
    def _check_cache_age(self, item: dict) -> bool:
        """Check if item has expired"""
        current_time = datetime.now()
        return (current_time - item['timestamp']).total_seconds() > self.max_age_seconds
    
    def set(self, key: str, value: Any, max_size: Optional[int] = None) -> None:
        """Securely store an item in the cache"""
        with self._lock:
            # Check size limit if provided
            if max_size is not None:
                self._check_cache_limits()
                self._total_size += max_size
            
            # Create cache path
            cache_path = self._get_cache_path(key)
            
            # Serialize and validate data
            try:
                serialized = json.dumps(value, default=str)
                item = {
                    'data': serialized,
                    'timestamp': datetime.now()
                }
                
                # Check cache age
                if cache_path.exists():
                    with open(cache_path, 'r') as f:
                        cached_item = json.load(f)
                    if not self._check_cache_age(cached_item):
                        os.remove(cache_path)
                
                # Write to file with secure permissions
                with tempfile.NamedTemporaryFile(mode='w', 
                                               dir=str(self.cache_dir),
                                               delete=False) as temp_file:
                    json.dump(item, temp_file)
                
                os.replace(temp_file.name, cache_path)
                self._total_size += len(serialized)
                
            except (TypeError, ValueError, OSError) as e:
                raise RuntimeError(f"Failed to cache item: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """Securely retrieve an item from the cache"""
        with self._lock:
            try:
                cache_path = self._