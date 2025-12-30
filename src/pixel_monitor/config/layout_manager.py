"""Layout save/load functionality"""

import json
from tkinter import filedialog, messagebox


class LayoutManager:
    """Manages saving and loading of layout configurations"""
    
    @staticmethod
    def save_layout(areas, parent_window=None):
        """Save all areas configuration to JSON file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Layout",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            parent=parent_window
        )
        
        if not file_path:
            return False
        
        # Prepare configuration data for all areas
        areas_config = []
        for area in areas:
            area_config = {
                "coordinates": area['coordinates'],
                "coordinates_condition": area['coordinates_condition'],
                "sound_file": area['sound_file'],
                "threshold": area['ui']['threshold_entry'].get(),
                "volume": area['ui']['volume_entry'].get(),
                "baseline_color": area['baseline_color'],
                "condition_color": area['condition_color'],
                "use_condition": area['use_condition'].get()
            }
            areas_config.append(area_config)
        
        config = {"areas": areas_config}
        
        try:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
            if parent_window:
                messagebox.showinfo("Success", f"Layout saved successfully!\n{len(areas_config)} area(s) saved.", parent=parent_window)
            return True
        except Exception as e:
            if parent_window:
                messagebox.showerror("Error", f"Failed to save layout:\n{e}", parent=parent_window)
            return False
    
    @staticmethod
    def load_layout(parent_window=None):
        """Load configuration from JSON file"""
        file_path = filedialog.askopenfilename(
            title="Load Layout",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            parent=parent_window
        )
        
        if not file_path:
            return None
        
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            
            # Validate the config structure
            if not isinstance(config, dict) or 'areas' not in config:
                raise ValueError("Invalid configuration format")
            
            return config, file_path
        except Exception as e:
            if parent_window:
                messagebox.showerror("Error", f"Failed to load layout:\n{e}", parent=parent_window)
            return None

