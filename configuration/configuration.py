"""Configuration management module for the Rubrik Daily Check application."""

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, ClassVar, Dict, Any

from services.validations import clear_empty_strings
from exceptions import ConfigurationError

logger = logging.getLogger(__name__)

@dataclass
class AppConfig:
    """Application configuration container."""
    
    # Class-level constants
    DEFAULT_TIMEZONE: ClassVar[str] = "UTC"
    
    # Instance variables
    root_dir: Path
    config_file: Path
    reports_dir: Path
    timezone: str
    client_id: str
    client_secret: str
    graphql_url: str
    access_token_uri: str
    google_drive_config: Optional[Path]
    google_drive_folder_ids: List[str]
    excluded_cluster_uuids: List[str]
    
    @classmethod
    def load(cls) -> 'AppConfig':
        """
        Load configuration from the config file.
        
        Returns:
            AppConfig: Initialized configuration object
            
        Raises:
            ConfigurationError: If configuration loading or validation fails
        """
        try:
            # Set up basic paths
            root_dir = Path(__file__).resolve().parent.parent
            config_file = root_dir / 'configuration' / 'config.json'
            reports_dir = root_dir / 'reports'
            google_config = root_dir / 'configuration' / 'google_drive.json'

            # Ensure config file exists
            if not config_file.exists():
                raise ConfigurationError(f"Configuration file not found: {config_file}")

            # Load and parse config file
            with open(config_file, 'r') as f:
                config_data = json.load(f)

            # Validate required fields
            required_fields = ['client_id', 'client_secret', 'graphql_url', 'access_token_uri']
            missing_fields = [field for field in required_fields if field not in config_data]
            if missing_fields:
                raise ConfigurationError(f"Missing required configuration fields: {', '.join(missing_fields)}")

            # Process optional fields with defaults
            timezone = config_data.get('tz_info', cls.DEFAULT_TIMEZONE)
            if not timezone:
                timezone = cls.DEFAULT_TIMEZONE
                logger.warning(f"Empty timezone specified, using default: {cls.DEFAULT_TIMEZONE}")

            # Process Google Drive configuration
            google_drive_config = google_config if google_config.exists() else None
            if not google_drive_config:
                logger.warning("Google Drive configuration file not found")

            # Process lists with empty string cleaning
            folder_ids = clear_empty_strings(config_data.get('google_drive_upload_folder_ids', []))
            cluster_uuids = clear_empty_strings(config_data.get('excluded_clusters_uuids', []))

            return cls(
                root_dir=root_dir,
                config_file=config_file,
                reports_dir=reports_dir,
                timezone=timezone,
                client_id=config_data['client_id'],
                client_secret=config_data['client_secret'],
                graphql_url=config_data['graphql_url'],
                access_token_uri=config_data['access_token_uri'],
                google_drive_config=google_drive_config,
                google_drive_folder_ids=folder_ids,
                excluded_cluster_uuids=cluster_uuids
            )

        except Exception as e:
            error_msg = "Failed to load configuration"
            logger.exception(error_msg)
            raise ConfigurationError(f"{error_msg}: {str(e)}") from e

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary format."""
        return {
            'root_dir': str(self.root_dir),
            'reports_dir': str(self.reports_dir),
            'timezone': self.timezone,
            'graphql_url': self.graphql_url,
            'access_token_uri': self.access_token_uri,
            'google_drive_config': str(self.google_drive_config) if self.google_drive_config else None,
            'google_drive_folder_ids': self.google_drive_folder_ids,
            'excluded_cluster_uuids': self.excluded_cluster_uuids
        }

# Global configuration instance
_config: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """
    Get the global configuration instance.
    
    Returns:
        AppConfig: The global configuration object
        
    Raises:
        ConfigurationError: If configuration loading fails
    """
    global _config
    if _config is None:
        _config = AppConfig.load()
    return _config

# Legacy compatibility functions
def load_config() -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    return get_config().to_dict()

def get_root_dir() -> str:
    """Legacy function for backward compatibility."""
    return str(get_config().root_dir)

def get_timezone_info() -> str:
    """Legacy function for backward compatibility."""
    return get_config().timezone

def get_google_config_path() -> Optional[str]:
    """Legacy function for backward compatibility."""
    config = get_config()
    if not config.google_drive_config:
        raise ValueError("Google Drive configuration file not found")
    return str(config.google_drive_config)

def get_drive_folder_id() -> Optional[List[str]]:
    """Legacy function for backward compatibility."""
    folders = get_config().google_drive_folder_ids
    return folders if folders else None

def get_excluded_clusters_uuids() -> Optional[List[str]]:
    """Legacy function for backward compatibility."""
    clusters = get_config().excluded_cluster_uuids
    return clusters if clusters else None
