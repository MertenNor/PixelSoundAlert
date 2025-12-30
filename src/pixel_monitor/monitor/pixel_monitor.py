"""Core pixel monitoring logic"""

import time
import threading
from .color_utils import ColorUtils


class PixelMonitor:
    """Handles pixel monitoring for areas"""
    
    def __init__(self, check_interval=0.05):
        self.check_interval = check_interval
        self.monitoring = False
        self.monitor_thread = None
        self.color_utils = ColorUtils()
    
    def start_monitoring(self, areas, update_callback, play_sound_callback):
        """Start monitoring all areas"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.areas = areas
        self.update_callback = update_callback
        self.play_sound_callback = play_sound_callback
        
        # Reset state for all areas
        for area in self.areas:
            area['color_changed'] = False
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_all_areas, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def _monitor_all_areas(self):
        """Monitor all areas simultaneously"""
        while self.monitoring:
            for area in self.areas:
                self._monitor_area(area)
            time.sleep(self.check_interval)
    
    def _monitor_area(self, area):
        """Monitor a single area"""
        current_color = self.color_utils.get_pixel_color_at(area['coordinates'])
        
        if current_color:
            # Update display
            if self.update_callback:
                self.update_callback(area['id'], current_color)
            
            # Check if color differs from baseline significantly
            threshold = self._get_threshold(area)
            if self.color_utils.color_difference(current_color, area['baseline_color']) > threshold:
                if not area['color_changed']:
                    # Pixel A changed from baseline!
                    should_play = True
                    
                    if area['use_condition'].get():
                        # Check if condition pixel (B) is the required color
                        if area['coordinates_condition'] and area['condition_color']:
                            condition_current = self.color_utils.get_pixel_color_at(area['coordinates_condition'])
                            if condition_current:
                                if self.color_utils.color_difference(condition_current, area['condition_color']) > threshold:
                                    should_play = False
                            else:
                                should_play = False
                        else:
                            should_play = False
                    
                    if should_play:
                        # Play sound!
                        area['color_changed'] = True
                        if self.play_sound_callback:
                            self.play_sound_callback(area)
            else:
                # Color returned to baseline
                if area['color_changed']:
                    area['color_changed'] = False
    
    def _get_threshold(self, area):
        """Get threshold value from area"""
        try:
            val = int(area['ui']['threshold_entry'].get())
            return max(0, min(100, val))
        except:
            return 30

