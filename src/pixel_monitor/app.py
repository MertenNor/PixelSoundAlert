"""Main application class"""

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

from .config import SettingsManager, LayoutManager
from .monitor import PixelMonitor, ColorUtils
from .audio import AudioPlayer
from .gui import MainWindow, AreaWidget


class PixelMonitorApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PixelSoundAlert")
        self.root.geometry("1050x400")
        self.root.resizable(True, True)
        self.root.minsize(900, 200)
        
        # Core variables
        self.areas = []  # List of area dictionaries
        self.area_counter = 0  # To assign unique IDs
        self.current_area_id = None  # Track which area is being edited
        
        # Initialize components
        self.settings_manager = SettingsManager()
        self.layout_manager = LayoutManager()
        self.pixel_monitor = PixelMonitor(check_interval=0.05)
        self.audio_player = AudioPlayer()
        self.color_utils = ColorUtils()
        
        # Setup GUI
        self.main_window = MainWindow(self.root, self)
        
        # Add first area by default
        self.add_area()
    
    def add_area(self):
        """Add a new monitoring area"""
        area_id = self.area_counter
        self.area_counter += 1
        
        # Create area data structure
        area = {
            'id': area_id,
            'coordinates': None,
            'coordinates_condition': None,
            'sound_file': None,
            'baseline_color': None,
            'condition_color': None,
            'color_changed': False,
            'use_condition': tk.BooleanVar(value=False),
            'ui': {}  # Store UI element references
        }
        
        self.areas.append(area)
        self._create_area_ui(area)
    
    def _create_area_ui(self, area):
        """Create UI for a single area"""
        callbacks = {
            'select_coordinates': self.select_coordinates,
            'select_coordinates_condition': self.select_coordinates_condition,
            'capture_baseline': self.capture_baseline_color,
            'capture_condition': self.capture_condition_color,
            'select_sound': self.select_sound,
            'toggle_condition': self.toggle_condition_ui,
            'remove_area': self.remove_area
        }
        
        AreaWidget(self.main_window.scrollable_frame, area, callbacks)
    
    def remove_area(self, area_id):
        """Remove an area"""
        if len(self.areas) <= 1:
            messagebox.showwarning("Warning", "Cannot remove the last area!")
            return
        
        # Find and remove area
        area = self.get_area_by_id(area_id)
        if area:
            # Destroy UI
            area['ui']['frame'].destroy()
            # Remove from list
            self.areas.remove(area)
    
    def get_area_by_id(self, area_id):
        """Get area by ID"""
        for area in self.areas:
            if area['id'] == area_id:
                return area
        return None
    
    def select_coordinates(self, area_id):
        """Let user click on screen to select coordinates"""
        self.main_window.create_coordinate_overlay(area_id, "A")
    
    def on_coordinate_selected(self, area_id, x, y):
        """Handle coordinate selection"""
        area = self.get_area_by_id(area_id)
        if area:
            area['coordinates'] = (x, y)
            area['ui']['coord_label'].config(text=f"X:{x} Y:{y}", fg="green")
            self.update_color_display(area_id)
    
    def capture_baseline_color(self, area_id):
        """Capture the current color at the selected pixel as baseline"""
        area = self.get_area_by_id(area_id)
        if not area:
            return
        
        if not area['coordinates']:
            messagebox.showwarning("Warning", "Please select coordinates first!")
            return
        
        current_color = self.color_utils.get_pixel_color_at(area['coordinates'])
        
        if current_color:
            area['baseline_color'] = current_color
            hex_color = self.color_utils.rgb_to_hex(current_color)
            area['ui']['baseline_display'].config(bg=hex_color)
        else:
            messagebox.showerror("Error", "Could not capture color!")
    
    def toggle_condition_ui(self, area_id):
        """Enable or disable condition UI elements"""
        area = self.get_area_by_id(area_id)
        if not area:
            return
        
        state = "normal" if area['use_condition'].get() else "disabled"
        area['ui']['coord_condition_btn'].config(state=state)
        area['ui']['coord_condition_label'].config(state=state)
        area['ui']['condition_display'].config(state=state)
        area['ui']['condition_btn'].config(state=state)
    
    def select_coordinates_condition(self, area_id):
        """Let user click on screen to select condition pixel (Pixel B)"""
        self.main_window.create_coordinate_overlay(area_id, "B")
    
    def on_condition_coordinate_selected(self, area_id, x, y):
        """Handle condition coordinate selection"""
        area = self.get_area_by_id(area_id)
        if area:
            area['coordinates_condition'] = (x, y)
            area['ui']['coord_condition_label'].config(text=f"X:{x} Y:{y}", fg="green")
    
    def capture_condition_color(self, area_id):
        """Capture the required color for condition pixel"""
        area = self.get_area_by_id(area_id)
        if not area:
            return
        
        if not area['coordinates_condition']:
            messagebox.showwarning("Warning", "Please select Pixel B coordinates first!")
            return
        
        current_color = self.color_utils.get_pixel_color_at(area['coordinates_condition'])
        
        if current_color:
            area['condition_color'] = current_color
            hex_color = self.color_utils.rgb_to_hex(current_color)
            area['ui']['condition_display'].config(bg=hex_color)
        else:
            messagebox.showerror("Error", "Could not capture color!")
    
    def select_sound(self, area_id):
        """Open file dialog to select sound file"""
        file_path = filedialog.askopenfilename(
            title=f"Select Sound File for Area {area_id + 1}",
            filetypes=[
                ("Audio Files", "*.wav *.mp3"), 
                ("WAV Files", "*.wav"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            area = self.get_area_by_id(area_id)
            if area:
                area['sound_file'] = file_path
                filename = file_path.split("/")[-1].split("\\")[-1]
                if len(filename) > 12:
                    filename = filename[:9] + "..."
                area['ui']['sound_label'].config(text=filename, fg="green")
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off for all areas"""
        if not self.pixel_monitor.monitoring:
            # Validate all areas
            for area in self.areas:
                area_num = area['id'] + 1
                if not area['coordinates']:
                    messagebox.showwarning("Warning", f"Area {area_num}: Please select coordinates!")
                    return
                if not area['sound_file']:
                    messagebox.showwarning("Warning", f"Area {area_num}: Please select a sound file!")
                    return
                if not area['baseline_color']:
                    messagebox.showwarning("Warning", f"Area {area_num}: Please capture baseline color!")
                    return
                
                if area['use_condition'].get():
                    if not area['coordinates_condition']:
                        messagebox.showwarning("Warning", f"Area {area_num}: Condition enabled but Pixel B not selected!")
                        return
                    if not area['condition_color']:
                        messagebox.showwarning("Warning", f"Area {area_num}: Condition enabled but Pixel B color not captured!")
                        return
            
            # Start monitoring
            self.main_window.update_toggle_button("STOP ALL", "#f44336")
            self.main_window.update_status("Monitoring all areas...", "green")
            
            self.pixel_monitor.start_monitoring(
                self.areas,
                self.update_color_display,
                self.audio_player.play_sound
            )
        else:
            # Stop monitoring
            self.pixel_monitor.stop_monitoring()
            self.main_window.update_toggle_button("START ALL", "#FF9800")
            self.main_window.update_status("Stopped", "gray")
    
    def update_color_display(self, area_id, color=None):
        """Update the color display canvas"""
        area = self.get_area_by_id(area_id)
        if not area:
            return
        
        if color is None:
            color = self.color_utils.get_pixel_color_at(area['coordinates'])
        
        if color:
            hex_color = self.color_utils.rgb_to_hex(color)
            area['ui']['color_display'].config(bg=hex_color)
            area['ui']['color_value_label'].config(text=f"RGB:\n{color[0]},{color[1]},{color[2]}")
    
    def load_layout_from_file(self, file_path, show_success=True):
        """Load configuration from a specific JSON file path"""
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            
            # Clear existing areas
            for area in self.areas[:]:
                area['ui']['frame'].destroy()
            self.areas.clear()
            self.area_counter = 0
            
            # Load areas
            if "areas" in config:
                for area_config in config["areas"]:
                    # Add new area
                    self.add_area()
                    area = self.areas[-1]
                    
                    # Load coordinates
                    if area_config.get("coordinates"):
                        area['coordinates'] = tuple(area_config["coordinates"]) if area_config["coordinates"] else None
                        if area['coordinates']:
                            area['ui']['coord_label'].config(
                                text=f"X:{area['coordinates'][0]} Y:{area['coordinates'][1]}", fg="green")
                    
                    if area_config.get("coordinates_condition"):
                        area['coordinates_condition'] = tuple(area_config["coordinates_condition"]) if area_config["coordinates_condition"] else None
                        if area['coordinates_condition']:
                            area['ui']['coord_condition_label'].config(
                                text=f"X:{area['coordinates_condition'][0]} Y:{area['coordinates_condition'][1]}", fg="green")
                    
                    # Load sound file
                    if area_config.get("sound_file"):
                        area['sound_file'] = area_config["sound_file"]
                        filename = area['sound_file'].split("/")[-1].split("\\")[-1]
                        if len(filename) > 12:
                            filename = filename[:9] + "..."
                        area['ui']['sound_label'].config(text=filename, fg="green")
                    
                    # Load threshold
                    if area_config.get("threshold"):
                        area['ui']['threshold_entry'].delete(0, tk.END)
                        area['ui']['threshold_entry'].insert(0, area_config["threshold"])
                    
                    # Load volume
                    if area_config.get("volume"):
                        area['ui']['volume_entry'].delete(0, tk.END)
                        area['ui']['volume_entry'].insert(0, area_config["volume"])
                    
                    # Load baseline color
                    if area_config.get("baseline_color"):
                        area['baseline_color'] = tuple(area_config["baseline_color"]) if area_config["baseline_color"] else None
                        if area['baseline_color']:
                            hex_color = self.color_utils.rgb_to_hex(area['baseline_color'])
                            area['ui']['baseline_display'].config(bg=hex_color)
                    
                    # Load condition color
                    if area_config.get("condition_color"):
                        area['condition_color'] = tuple(area_config["condition_color"]) if area_config["condition_color"] else None
                        if area['condition_color']:
                            hex_color = self.color_utils.rgb_to_hex(area['condition_color'])
                            area['ui']['condition_display'].config(bg=hex_color)
                    
                    # Load use_condition
                    if "use_condition" in area_config:
                        area['use_condition'].set(area_config["use_condition"])
                        self.toggle_condition_ui(area['id'])
            
            if show_success:
                messagebox.showinfo("Success", f"Layout loaded successfully!\n{len(self.areas)} area(s) loaded.")
            
        except Exception as e:
            raise Exception(f"Failed to load layout: {str(e)}")
    
    def save_layout(self):
        """Save all areas configuration to JSON file"""
        success = self.layout_manager.save_layout(self.areas, self.root)
        if success:
            # Note: We could update last loaded file here if desired
            pass
    
    def load_layout(self):
        """Load configuration from JSON file"""
        result = self.layout_manager.load_layout(self.root)
        if result:
            config, file_path = result
            try:
                self.load_layout_from_file(file_path, show_success=True)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)

