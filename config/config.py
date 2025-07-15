
"""
Configuration management for the Quote Maker application.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages application configuration from multiple sources."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the ConfigManager.
        
        Args:
            config_file: Path to configuration file (optional)
        """
        self.logger = logging.getLogger(__name__)
        self.config_data: Dict[str, Any] = {}
        self._load_defaults()
        
        if config_file:
            self._load_from_file(config_file)
        
        self._load_from_env()
    
    def _load_defaults(self):
        """Load default configuration values."""
        self.config_data = {
            # Font settings
            'FONT_PATH': 'src/quote_maker/fonts/Quote.ttf',
            'FONT_SIZE': 50,
            
            # Image settings
            'IMAGE_TYPE': 'RGBA',
            'IMAGE_WIDTH': 1200,
            'IMAGE_HEIGHT': 600,
            'IMAGE_BG_COLORS': [(255, 0, 0), (51, 0, 51), (0, 0, 255), (0, 0, 0)],
            
            # Facebook API settings
            'FACEBOOK_PAGE_ID': 'your_page_id',
            'FACEBOOK_ACCESS_TOKEN': None,
            
            # Quote sources
            'DEFAULT_QUOTE_SOURCE': 'manual',
            'QUOTE_API_URL': 'https://api.quotable.io/random',
            'QUOTE_FILE_PATH': 'quotes.json',
            
            # Logging settings
            'LOG_LEVEL': 'INFO',
            'LOG_FILE': 'quote_maker.log',
        }
    
    def _load_from_file(self, config_file: str):
        """Load configuration from a JSON file."""
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self.config_data.update(file_config)
                    self.logger.info(f"Configuration loaded from {config_file}")
            else:
                self.logger.warning(f"Configuration file not found: {config_file}")
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading configuration file: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'FACEBOOK_ACCESS_TOKEN': 'FACEBOOK_ACCESS_TOKEN',
            'FACEBOOK_PAGE_ID': 'FACEBOOK_PAGE_ID',
            'QUOTE_API_URL': 'QUOTE_API_URL',
            'LOG_LEVEL': 'LOG_LEVEL',
        }
        
        for config_key, env_key in env_mappings.items():
            env_value = os.environ.get(env_key)
            if env_value:
                self.config_data[config_key] = env_value
                self.logger.debug(f"Loaded {config_key} from environment")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config_data[key] = value
    
    def update(self, config_dict: Dict[str, Any]):
        """
        Update configuration with a dictionary.
        
        Args:
            config_dict: Dictionary of configuration values
        """
        self.config_data.update(config_dict)
    
    def save_to_file(self, config_file: str):
        """
        Save current configuration to a file.
        
        Args:
            config_file: Path to save configuration
        """
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2)
            self.logger.info(f"Configuration saved to {config_file}")
        except IOError as e:
            self.logger.error(f"Error saving configuration: {e}")
    
    def __getattr__(self, name: str) -> Any:
        """Allow attribute-style access to configuration values."""
        if name in self.config_data:
            return self.config_data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any):
        """Allow attribute-style setting of configuration values."""
        if name in ['config_data', 'logger']:
            super().__setattr__(name, value)
        else:
            if hasattr(self, 'config_data'):
                self.config_data[name] = value
            else:
                super().__setattr__(name, value)


# Global configuration instance for backward compatibility
_config_manager = ConfigManager()

# Expose configuration values as module-level attributes for backward compatibility
FONT_PATH = _config_manager.FONT_PATH
FONT_SIZE = _config_manager.FONT_SIZE
IMAGE_TYPE = _config_manager.IMAGE_TYPE
IMAGE_WIDTH = _config_manager.IMAGE_WIDTH
IMAGE_HEIGHT = _config_manager.IMAGE_HEIGHT
IMAGE_BG_COLORS = _config_manager.IMAGE_BG_COLORS
FACEBOOK_PAGE_ID = _config_manager.FACEBOOK_PAGE_ID
FACEBOOK_ACCESS_TOKEN = _config_manager.FACEBOOK_ACCESS_TOKEN
