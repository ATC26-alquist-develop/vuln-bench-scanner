```python
import os
import pickle
import hashlib
import tempfile
import shutil
from typing import Any, Dict
from pathlib import Path
import time

class SecureDiskCache:
    def __init__(self, cache_dir: str, max_size_mb: int = 100, max_age_days: int = 30):
        """Initialize secure disk cache with strict controls."""
        # Create secure cache directory
        self.cache_dir = Path(cache_dir).resolve()
        self.max_size = max_size_mb * 1024 * 1024  # Convert to bytes
        self.max_age = max_age_days * 24 * 60 * 60  # Convert to seconds
        
        # Ensure cache directory exists and is secure
        self._create_secure_cache_dir()
        
        # Initialize cache storage
        self._cache: Dict[str, Any] = {}
        self._load_existing_cache()

    def _create_secure_cache_dir(self) -> None:
        """Create cache directory with secure permissions."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(self.cache_dir, 0o700)  # Restrict permissions to owner only
        except OSError as e:
            raise SecurityError(f"Failed to create cache directory: {e}")

    def _load_existing_cache(self) -> None:
        """Securely load existing cache from disk."""
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = (self.cache_dir / filename).resolve()
                if file_path.is_file() and file_path.suffix == '.cache':
                    try:
                        with open(file_path, 'rb') as f:
                            key = hashlib.sha256(f.read()).hexdigest()
                            self._cache[key] = pickle.load(f)
                    except (pickle.UnpicklingError, EOFError, OSError) as e:
                        print(f"Warning: Skipping invalid cache file {file_path}")
        except OSError as e:
            raise SecurityError(f"Failed to load existing cache: {e}")

    def _get_cache_path(self, key: str) -> Path:
        """Generate secure cache file path."""
        return (self.cache_dir / f"{hashlib.sha256(key.encode()).hexdigest()}.cache").resolve()

    def _check_cache_size(self) -> None:
        """Check and enforce cache size limits."""
        total_size = sum(os.path.getsize(f) for f in self.cache_dir.glob('*.cache') if f.is_file())
        if total_size > self.max_size:
            self._prune_cache()

    def _prune_cache(self) -> None:
        """Securely remove oldest cache entries to enforce size limits."""
        sorted_files = sorted(
            (f for f in self.cache_dir.glob('*.cache') if f.is_file()),
            key=lambda f: os.path.getmtime(f)
        )
        while sorted_files and total_size > self.max_size:
            oldest = sorted_files.pop(0)
            try:
                os.remove(oldest)
                total_size -= oldest.stat().st_size
            except OSError as e:
                print(f"Warning: Unable to remove cache file {oldest}: {e}")

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Securely store object in cache with optional TTL."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        
        cache_path = self._get_cache_path(key)
        try:
            # Serialize and encrypt data
            serialized = pickle.dumps(value)
            encrypted = self._encrypt_data(serialized)
            
            # Write to cache file
            with open(cache_path, 'wb') as f:
                f.write(encrypted)
            
            # Update cache dictionary
            self._cache[key] = value
            
            # Set TTL if provided