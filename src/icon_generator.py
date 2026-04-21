"""Generate dynamic SVG icons for temperature display."""

import os
import tempfile
from pathlib import Path


class IconGenerator:
    """Generate SVG icons for different temperature states."""

    # Color definitions
    COLORS = {
        "green": {"bg": "#4CAF50", "text": "#FFFFFF"},  # Normal (< 50°C)
        "amber": {"bg": "#FFC107", "text": "#000000"},  # Warm (50-80°C)
        "red": {"bg": "#F44336", "text": "#FFFFFF"},  # Hot (> 80°C)
    }

    def __init__(self):
        """Initialize icon generator."""
        self.icon_cache = {}
        self.temp_dir = Path(tempfile.gettempdir()) / "tempicon_icons"
        self.temp_dir.mkdir(exist_ok=True)

    def get_color_for_temp(self, temp):
        """
        Get color name for temperature.

        Args:
            temp: Temperature in Celsius

        Returns:
            Color name (green, amber, or red)
        """
        if temp < 50:
            return "green"
        elif temp < 80:
            return "amber"
        else:
            return "red"

    def generate_icon_path(self, temp, icon_style="square"):
        """
        Generate or retrieve cached icon path.

        Args:
            temp: Temperature value
            icon_style: Style of icon ('square', 'circle', or 'text')

        Returns:
            Path to the icon file
        """
        color = self.get_color_for_temp(temp)
        display_temp = f"{temp:.0f}"

        # Cache key
        cache_key = f"{color}_{display_temp}_{icon_style}"

        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]

        # Generate SVG
        if icon_style == "square":
            svg_content = self._generate_square_icon(display_temp, color)
        elif icon_style == "circle":
            svg_content = self._generate_circle_icon(display_temp, color)
        else:  # text style
            svg_content = self._generate_text_icon(display_temp, color)

        # Save to temporary file
        icon_path = self.temp_dir / f"{cache_key}.svg"
        with open(icon_path, "w") as f:
            f.write(svg_content)

        self.icon_cache[cache_key] = str(icon_path)
        return str(icon_path)

    def _generate_square_icon(self, temp_str, color):
        """Generate square colored icon with temperature."""
        color_info = self.COLORS[color]
        bg_color = color_info["bg"]
        text_color = color_info["text"]

        # Calculate font size based on text length
        font_size = 28 if len(temp_str) <= 2 else 20

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <!-- Background square -->
  <rect width="48" height="48" rx="4" ry="4" fill="{bg_color}"/>
  
  <!-- Temperature text -->
  <text x="24" y="32" font-family="Arial, sans-serif" font-size="{font_size}" 
        font-weight="bold" text-anchor="middle" fill="{text_color}">
    {temp_str}
  </text>
</svg>"""
        return svg

    def _generate_circle_icon(self, temp_str, color):
        """Generate circular colored icon with temperature."""
        color_info = self.COLORS[color]
        bg_color = color_info["bg"]
        text_color = color_info["text"]

        # Calculate font size based on text length
        font_size = 28 if len(temp_str) <= 2 else 20

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <!-- Background circle -->
  <circle cx="24" cy="24" r="24" fill="{bg_color}"/>
  
  <!-- Temperature text -->
  <text x="24" y="32" font-family="Arial, sans-serif" font-size="{font_size}" 
        font-weight="bold" text-anchor="middle" fill="{text_color}">
    {temp_str}
  </text>
</svg>"""
        return svg

    def _generate_text_icon(self, temp_str, color):
        """Generate text-only icon (simple label)."""
        color_info = self.COLORS[color]
        text_color = color_info["bg"]

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <!-- Transparent background for tray -->
  
  <!-- Temperature text -->
  <text x="24" y="32" font-family="Arial, sans-serif" font-size="24" 
        font-weight="bold" text-anchor="middle" fill="{text_color}">
    {temp_str}
  </text>
</svg>"""
        return svg

    def cleanup(self):
        """Clean up temporary icon files."""
        try:
            import shutil

            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Warning: Could not cleanup icon temp directory: {e}")
