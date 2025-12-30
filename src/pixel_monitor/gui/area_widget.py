"""Area widget UI component"""

import tkinter as tk
from ..monitor.color_utils import ColorUtils


class AreaWidget:
    """UI widget for a single monitoring area"""
    
    def __init__(self, parent_frame, area, callbacks):
        """
        Initialize area widget
        
        Args:
            parent_frame: Parent frame to pack into
            area: Area dictionary with configuration
            callbacks: Dictionary of callback functions
        """
        self.area = area
        self.callbacks = callbacks
        self.color_utils = ColorUtils()
        self._create_ui(parent_frame)
    
    def _create_ui(self, parent_frame):
        """Create UI for a single area"""
        area_id = self.area['id']
        
        # Main frame for this area
        area_frame = tk.LabelFrame(
            parent_frame, 
            text=f"Area {area_id + 1}", 
            padx=5, 
            pady=5, 
            font=("Arial", 10, "bold"),
            relief="raised", 
            borderwidth=2
        )
        area_frame.pack(fill="x", padx=5, pady=5)
        
        self.area['ui']['frame'] = area_frame
        
        # Main row container
        main_row = tk.Frame(area_frame)
        main_row.pack(fill="x", padx=2, pady=2)
        
        # Column 1: Pixel A
        col1 = tk.LabelFrame(main_row, text="Pixel A", padx=2, pady=1, font=("Arial", 10, "bold"))
        col1.pack(side="left", fill="both", expand=True, padx=2)
        
        pixel_a_row = tk.Frame(col1)
        pixel_a_row.pack(fill="x", padx=2, pady=1)
        
        tk.Button(
            pixel_a_row, 
            text="Select", 
            command=lambda: self.callbacks['select_coordinates'](area_id),
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 8), 
            width=5
        ).pack(side="left", padx=1)
        
        coord_label = tk.Label(pixel_a_row, text="Not set", fg="gray", font=("Arial", 8))
        coord_label.pack(side="left", padx=1)
        self.area['ui']['coord_label'] = coord_label
        
        tk.Label(pixel_a_row, text="Color:", font=("Arial", 8)).pack(side="left", padx=1)
        baseline_display = tk.Canvas(
            pixel_a_row, 
            width=30, 
            height=18, 
            bg="white", 
            relief="solid", 
            borderwidth=1
        )
        baseline_display.pack(side="left", padx=1)
        self.area['ui']['baseline_display'] = baseline_display
        
        tk.Button(
            pixel_a_row, 
            text="Capture", 
            command=lambda: self.callbacks['capture_baseline'](area_id),
            bg="#9C27B0", 
            fg="white", 
            font=("Arial", 8), 
            width=5
        ).pack(side="left", padx=1)
        
        # Column 2: Pixel B
        col2 = tk.LabelFrame(main_row, text="Pixel B", padx=2, pady=1, font=("Arial", 10, "bold"))
        col2.pack(side="left", fill="both", expand=True, padx=2)
        
        pixel_b_row = tk.Frame(col2)
        pixel_b_row.pack(fill="x", padx=2, pady=1)
        
        enable_check = tk.Checkbutton(
            pixel_b_row, 
            text="Enable", 
            variable=self.area['use_condition'],
            command=lambda: self.callbacks['toggle_condition'](area_id), 
            font=("Arial", 8)
        )
        enable_check.pack(side="left", padx=1)
        
        coord_condition_btn = tk.Button(
            pixel_b_row, 
            text="Select", 
            command=lambda: self.callbacks['select_coordinates_condition'](area_id),
            bg="#FF5722", 
            fg="white", 
            font=("Arial", 8), 
            width=5
        )
        coord_condition_btn.pack(side="left", padx=1)
        self.area['ui']['coord_condition_btn'] = coord_condition_btn
        
        coord_condition_label = tk.Label(pixel_b_row, text="Not set", fg="gray", font=("Arial", 8))
        coord_condition_label.pack(side="left", padx=1)
        self.area['ui']['coord_condition_label'] = coord_condition_label
        
        tk.Label(pixel_b_row, text="Color:", font=("Arial", 8)).pack(side="left", padx=1)
        condition_display = tk.Canvas(
            pixel_b_row, 
            width=30, 
            height=18, 
            bg="white", 
            relief="solid", 
            borderwidth=1
        )
        condition_display.pack(side="left", padx=1)
        self.area['ui']['condition_display'] = condition_display
        
        condition_btn = tk.Button(
            pixel_b_row, 
            text="Capture", 
            command=lambda: self.callbacks['capture_condition'](area_id),
            bg="#FF5722", 
            fg="white", 
            font=("Arial", 8), 
            width=5
        )
        condition_btn.pack(side="left", padx=1)
        self.area['ui']['condition_btn'] = condition_btn
        
        # Explanation text
        info_label = tk.Label(
            col2, 
            text="Sound plays only if Pixel B matches captured color", 
            font=("Arial", 8), 
            fg="black"
        )
        info_label.pack(pady=1)
        
        self.callbacks['toggle_condition'](area_id)
        
        # Column 3: Sound
        col3 = tk.LabelFrame(main_row, text="Sound", padx=2, pady=1, font=("Arial", 10, "bold"))
        col3.pack(side="left", fill="both", expand=True, padx=2)
        
        sound_row = tk.Frame(col3)
        sound_row.pack(fill="x", padx=2, pady=1)
        
        tk.Button(
            sound_row, 
            text="Browse", 
            command=lambda: self.callbacks['select_sound'](area_id),
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 8), 
            width=5
        ).pack(side="left", padx=1)
        
        sound_label = tk.Label(
            sound_row, 
            text="None", 
            fg="gray", 
            font=("Arial", 8), 
            wraplength=100
        )
        sound_label.pack(side="left", padx=1)
        self.area['ui']['sound_label'] = sound_label
        
        # Column 4: Settings
        col4 = tk.LabelFrame(main_row, text="Settings", padx=2, pady=1, font=("Arial", 10, "bold"))
        col4.pack(side="left", fill="both", expand=True, padx=2)
        
        settings_row = tk.Frame(col4)
        settings_row.pack(fill="x", padx=2, pady=1)
        
        tk.Label(settings_row, text="Threshold", font=("Arial", 8)).pack(side="left", padx=1)
        threshold_entry = tk.Entry(settings_row, width=5, font=("Arial", 8), justify="center")
        threshold_entry.insert(0, "30")
        threshold_entry.pack(side="left", padx=1)
        self.area['ui']['threshold_entry'] = threshold_entry
        
        tk.Label(settings_row, text="Volume", font=("Arial", 8)).pack(side="left", padx=1)
        volume_entry = tk.Entry(settings_row, width=5, font=("Arial", 8), justify="center")
        volume_entry.insert(0, "50")
        volume_entry.pack(side="left", padx=1)
        self.area['ui']['volume_entry'] = volume_entry
        
        # Column 5: Live
        col5 = tk.LabelFrame(main_row, text="Live", padx=2, pady=1, font=("Arial", 10, "bold"))
        col5.pack(side="left", fill="both", expand=True, padx=2)
        
        live_row = tk.Frame(col5)
        live_row.pack(fill="x", padx=2, pady=1)
        
        color_display = tk.Canvas(
            live_row, 
            width=35, 
            height=25, 
            bg="white", 
            relief="solid", 
            borderwidth=1
        )
        color_display.pack(side="left", padx=1)
        self.area['ui']['color_display'] = color_display
        
        color_value_label = tk.Label(
            live_row, 
            text="RGB:\n---", 
            font=("Arial", 8), 
            justify="center"
        )
        color_value_label.pack(side="left", padx=1)
        self.area['ui']['color_value_label'] = color_value_label
        
        # Remove button
        remove_btn = tk.Button(
            main_row, 
            text="❌", 
            command=lambda: self.callbacks['remove_area'](area_id),
            bg="#f44336", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=3
        )
        remove_btn.pack(side="left", padx=2)

