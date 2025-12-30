"""Color comparison and pixel capture utilities"""

from PIL import ImageGrab


class ColorUtils:
    """Utility functions for color operations"""
    
    @staticmethod
    def get_pixel_color_at(coords):
        """Get the color of the pixel at specified coordinates"""
        if not coords:
            return None
        
        try:
            x, y = coords
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel = screenshot.getpixel((0, 0))
            return pixel[:3] if len(pixel) > 3 else pixel
        except Exception as e:
            print(f"Error capturing pixel: {e}")
            return None
    
    @staticmethod
    def color_difference(color1, color2):
        """Calculate the difference between two RGB colors"""
        if not color1 or not color2:
            return float('inf')
        
        r_diff = abs(color1[0] - color2[0])
        g_diff = abs(color1[1] - color2[1])
        b_diff = abs(color1[2] - color2[2])
        return max(r_diff, g_diff, b_diff)
    
    @staticmethod
    def rgb_to_hex(color):
        """Convert RGB tuple to hex color string"""
        if not color:
            return "#000000"
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

