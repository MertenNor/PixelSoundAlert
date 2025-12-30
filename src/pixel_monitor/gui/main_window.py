"""Main window GUI setup"""

import tkinter as tk
from tkinter import filedialog, messagebox
from ..monitor.color_utils import ColorUtils
from .area_widget import AreaWidget


class MainWindow:
    """Main application window"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.color_utils = ColorUtils()
        self._setup_gui()
    
    def _setup_gui(self):
        """Setup the main GUI"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="PixelSoundAlert", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=3)
        
        # Control buttons at top
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Button(
            control_frame, 
            text="Save Layout", 
            command=self.app.save_layout,
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=10
        ).pack(side="left", padx=2)
        
        tk.Button(
            control_frame, 
            text="Load Layout", 
            command=self.app.load_layout,
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=10
        ).pack(side="left", padx=2)
        
        self.toggle_btn = tk.Button(
            control_frame, 
            text="START Monitoring all areas", 
            command=self.app.toggle_monitoring,
            bg="#FF9800", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=25
        )
        self.toggle_btn.pack(side="left", padx=2)
        
        # Add Area Button
        add_area_frame = tk.Frame(self.root)
        add_area_frame.pack(fill="x", padx=10, pady=2)
        
        tk.Button(
            add_area_frame, 
            text="➕ Add Area", 
            command=self.app.add_area,
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=2)
        
        self.status_label = tk.Label(
            add_area_frame, 
            text="Idle", 
            font=("Arial", 9), 
            fg="gray"
        )
        self.status_label.pack(side="left", padx=10)
        
        # Scrollable frame for areas
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5, padx=(0, 10))
    
    def update_status(self, text, color="gray"):
        """Update status label"""
        self.status_label.config(text=text, fg=color)
    
    def update_toggle_button(self, text, color):
        """Update toggle button"""
        self.toggle_btn.config(text=text, bg=color)
    
    def create_coordinate_overlay(self, area_id, pixel_type="A"):
        """Create overlay for coordinate selection"""
        self.app.current_area_id = area_id
        overlay = tk.Toplevel(self.root)
        overlay.attributes('-fullscreen', True)
        overlay.attributes('-alpha', 0.3)
        overlay.attributes('-topmost', True)
        
        bg_color = 'black' if pixel_type == "A" else 'blue'
        overlay.config(bg=bg_color, cursor='crosshair')
        
        instruction = tk.Label(
            overlay, 
            text=f"Area {area_id + 1} - Click to select Pixel {pixel_type}\nESC to cancel",
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg='white'
        )
        instruction.pack(pady=50)
        
        def on_click(event):
            x = overlay.winfo_pointerx()
            y = overlay.winfo_pointery()
            overlay.destroy()
            if pixel_type == "A":
                self.app.on_coordinate_selected(area_id, x, y)
            else:
                self.app.on_condition_coordinate_selected(area_id, x, y)
        
        def cancel(event):
            overlay.destroy()
            self.app.current_area_id = None
        
        overlay.bind('<Button-1>', on_click)
        overlay.bind('<Escape>', cancel)
        overlay.focus_set()
        
        return overlay

