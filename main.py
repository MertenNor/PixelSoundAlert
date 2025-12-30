"""Main entry point for Pixel Monitor application"""

import tkinter as tk
from src.pixel_monitor.app import PixelMonitorApp


def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = PixelMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

