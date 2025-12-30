"""Settings file management"""

import json
import os


class SettingsManager:
    """Manages application settings stored in a local config file"""
    
    def __init__(self, config_file_path=None):
        """
        Initialize settings manager
        
        Args:
            config_file_path: Path to config file. If None, uses 'config.json' in current working directory
        """
        if config_file_path is None:
            # Default to config.json in the current working directory (where the app is run from)
            config_file_path = os.path.join(os.getcwd(), 'config.json')
        
        self.settings_file = config_file_path
    
    def read_settings(self):
        """Read settings from the settings JSON file"""
        if not os.path.exists(self.settings_file):
            return {}
        
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading settings: {e}")
            return {}
    
    def write_settings(self, settings):
        """Write settings to the settings JSON file"""
        # Ensure directory exists, but don't call _ensure_settings_file to avoid recursion
        settings_dir = os.path.dirname(self.settings_file)
        if settings_dir and not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error writing settings: {e}")
    
    def update_last_loaded_file(self, file_path):
        """Update the settings file with the latest loaded file path"""
        settings = self.read_settings()
        settings['last_loaded_file'] = file_path
        self.write_settings(settings)
    
    def clear_last_loaded_file(self):
        """Clear the last loaded file path from settings"""
        settings = self.read_settings()
        if 'last_loaded_file' in settings:
            del settings['last_loaded_file']
        self.write_settings(settings)
    
    def get_last_loaded_file(self):
        """Get the last loaded file path from settings"""
        settings = self.read_settings()
        return settings.get('last_loaded_file')

