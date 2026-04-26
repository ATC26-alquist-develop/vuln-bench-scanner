import configparser
import os
import stat
import logging
from pathlib import Path
from typing import Dict, Optional

class SecureConfig:
    def __init__(self, config_path: str):
        """Initialize secure config with proper permissions."""
        self.config_path = Path(config_path).resolve()
        self.config = configparser.ConfigParser()
        
        # Ensure config directory exists with secure permissions
        self._create_secure_directory()
        
        # Set secure permissions (only owner can read/write)
        self._set_secure_permissions()
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _create_secure_directory(self) -> None:
        """Create config directory with secure permissions."""
        try:
            self.config_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            self.logger.error(f"Failed to create config directory: {e}")
            raise

    def _set_secure_permissions(self) -> None:
        """Set secure permissions on config file."""
        try:
            os.chmod(self.config_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError as e:
            self.logger.error(f"Failed to set config file permissions: {e}")
            raise

    def get(self, section: str, key: str, default: Optional[str] = None) -> Optional[str]:
        """Safely retrieve config value."""
        if not self.config_path.exists():
            return default
            
        try:
            self.config.read(self.config_path)
            if not self.config.has_section(section):
                return default
            if not self.config.has_option(section, key):
                return default
            return self.config.get(section, key)
        except (configparser.Error, OSError) as e:
            self.logger.error(f"Error reading config: {e}")
            return default

    def set(self, section: str, key: str, value: str) -> None:
        """Safely set config value."""
        try:
            if not self.config_path.exists():
                self.config.add_section(section)
            
            self.config.set(section, key, value)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            
            # Set secure permissions after writing
            os.chmod(self.config_path, stat.S_IRUSR | stat.S_IWUSR)
        except (configparser.Error, OSError) as e:
            self.logger.error(f"Error writing config: {e}")

    def delete(self, section: str, key: str) -> None:
        """Safely delete config value."""
        try:
            if not self.config_path.exists():
                return

            self.config.remove_option(section, key)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            
            # Set secure permissions after writing
            os.chmod(self.config_path, stat.S_IRUSR | stat.S_IWUSR)
        except (configparser.Error, OSError) as e:
            self.logger.error(f"Error deleting config: {e}")