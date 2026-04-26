import paramiko
import logging
from typing import Optional
from pathlib import Path
import os

class SecureSSHClient:
    def __init__(self, config_path: str):
        """Initialize SSH client with secure configuration."""
        # Validate config file path
        self.config_path = Path(config_path).resolve()
        if not self.config_path.is_file():
            raise ValueError("Config file does not exist")
            
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configuration securely
        self._load_config()
        
    def _load_config(self) -> None:
        """Load SSH configuration from file securely."""
        try:
            with open(self.config_path, 'r') as f:
                # Use safe parsing to prevent code injection
                config = paramiko.SSHConfig()
                config.parse(f)
                
            self.config = config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise

    def connect(self, hostname: str, username: str) -> Optional[paramiko.SSHClient]:
        """Establish secure SSH connection."""
        try:
            # Validate inputs
            if not all([hostname, username]):
                raise ValueError("Hostname and username must be provided")
                
            # Create SSH client
            client = paramiko.SSHClient()
            
            # Load system host keys
            client.load_system_host_keys()
            
            # Set timeout
            client.set_missing_host_key_policy(paramiko.RejectPolicy())
            
            # Connect with validated parameters
            client.connect(
                hostname=hostname,
                username=username,
                key_filename=self.config_path,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            return client
            
        except Exception as e:
            self.logger.error(f"SSH connection failed: {e}")
            return None

    def close(self, client: paramiko.SSHClient) -> None:
        """Safely close SSH connection."""
        if client:
            client.close()