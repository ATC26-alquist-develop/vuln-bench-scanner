import os
import json
import hashlib
import tempfile
import time
from typing import Any, Dict
from pathlib import Path
from functools import wraps

class SecureDiskCache:
    def __init__(self, 
                 max_size_mb: int = 100, 
                 max_age_seconds: int = 3600):
        """
        Initialize secure disk cache with size limits and expiration
        
        Args:
            max_size_mb: Maximum cache size in MB
            max_age_seconds: Maximum cache age in seconds
        """
        self.max_size_mb = max_size_mb
        self.max_age_seconds = max_age_seconds
        self.cache_dir = Path(tempfile.gettempdir()) / "secure_cache"
        self.cache: Dict[str, Dict[str, Any]] = {}
        
        # Ensure cache directory exists with secure permissions
        self.cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Generate secure path for cache file"""
        # Use SHA256 for consistent hashing
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.json"

    def _check_size(self) -> None:
        """Check if cache size exceeds limit"""
        current_size = sum(f.stat().st_size for f in self.cache_dir.glob('*'))
        if current_size > self.max_size_mb * 1024 * 1024:
            self._cleanup()

    def _cleanup(self) -> None:
        """Remove oldest cache entries if size limit is exceeded"""
        cache_files = list(self.cache_dir.glob('*'))
        if len(cache_files) > self.max_size_mb:
            oldest_file = min(cache_files, key=lambda f: f.stat().st_mtime)
            oldest_file.unlink()

    def _check_expiration(self, key: str) -> bool:
        """Check if cache entry has expired"""
        if key not in self.cache:
            return False
        if time.time() - self.cache[key]['timestamp'] > self.max_age_seconds:
            return True
        return False

    def set(self, key: str, value: Any) -> None:
        """Securely set cache entry"""
        self._check_size()
        
        # Validate input
        if not isinstance(key, str) or not key:
            raise ValueError("Invalid cache key")
            
        # Create secure path
        cache_path = self._get_cache_path(key)
        
        # Store with expiration
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        
        # Write to file with secure permissions
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.cache[key], f)
        os.chmod(cache_path, 0o600)

    def get(self, key: str) -> Any:
        """Securely retrieve cache entry"""
        self._check_size()
        
        # Validate input
        if not isinstance(key, str) or not key:
            raise ValueError("Invalid cache key")
            
        if key not in self.cache:
            return None
            
        if self._check_expiration(key):
            del self.cache[key]
            return None
            
        # Read from file with secure permissions
        cache_path = self._get_cache_path(key)
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['value']

    def clear(self) -> None:
        """Securely clear all cache entries"""
        for file in self.cache_dir.glob('*'):
            file.unlink()
        self.cache.clear()