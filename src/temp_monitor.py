#!/usr/bin/env python3
"""Main TempIcon application - CPU temperature system tray monitor."""

import gi
import sys
import signal
from pathlib import Path

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gtk, Gdk, GLib
from gi.repository import AppIndicator3 as appindicator
from temp_reader import TemperatureReader
from config_manager import ConfigManager
from settings_dialog import SettingsDialog


class TempIconApp:
    """Main application class for TempIcon."""

    def __init__(self):
        """Initialize the application."""
        self.temp_reader = TemperatureReader()
        self.config_manager = ConfigManager()
        self.indicator = None
        self.current_temp = None
        self.update_timeout = None

        # Create window (hidden)
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(1, 1)
        self.window.set_keep_above(True)
        self.window.set_decorated(False)
        self.window.move(-9999, -9999)  # Move off-screen

        self._setup_cleanup()

    def _setup_cleanup(self):
        """Setup cleanup on window close."""
        self.window.connect("delete-event", self._on_window_delete)
        signal.signal(signal.SIGINT, self._on_signal)
        signal.signal(signal.SIGTERM, self._on_signal)

    def _on_signal(self, sig, frame):
        """Handle system signals."""
        self.quit()

    def _on_window_delete(self, widget, event):
        """Handle window delete event."""
        return self._on_tray_quit()

    def run(self):
        """Run the application."""
        self._setup_indicator()
        self._start_update_loop()

        try:
            Gtk.main()
        except KeyboardInterrupt:
            self.quit()

    def _setup_indicator(self):
        """Setup system tray indicator with AppIndicator3."""
        self.indicator = appindicator.Indicator.new(
            "tempicon",
            "",
            appindicator.IndicatorCategory.SYSTEM_SERVICES,
        )

        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # Create menu (required for indicator to display)
        menu = Gtk.Menu()

        # Settings menu item
        settings_item = Gtk.MenuItem("Settings")
        settings_item.connect("activate", self._on_settings_clicked)
        menu.append(settings_item)

        # Quit menu item
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate", self._on_tray_quit)
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def _start_update_loop(self):
        """Start the temperature update loop."""
        self._update_temperature()

    def _update_temperature(self):
        """Update temperature and indicator."""
        temp = self.temp_reader.get_cpu_temperature()
        self.current_temp = temp

        # Update indicator display
        if temp is not None:
            # Get icon style preference
            icon_style = self.config_manager.get("icon_style", "square")

            # Get configured temperature thresholds
            temp_green_max = self.config_manager.get("temp_green_max", 50)
            temp_red_min = self.config_manager.get("temp_red_min", 80)

            # Convert to Fahrenheit if configured
            display_temp = temp
            unit = "°C"

            if self.config_manager.get("show_fahrenheit", False):
                display_temp = (temp * 9 / 5) + 32
                unit = "°F"

            status = self.temp_reader.get_status_text(temp)

            label_text = f"{display_temp:.0f}°"

            # Get symbol for icon style based on configured thresholds
            if icon_style == "square":
                # Use colored square symbol
                if temp < temp_green_max:
                    symbol = "🟩"  # Green square
                elif temp < temp_red_min:
                    symbol = "🟨"  # Yellow/Amber square
                else:
                    symbol = "🟥"  # Red square
                self.indicator.set_label(f"{symbol} {label_text}", "")
            elif icon_style == "circle":
                # Use colored circle symbol
                if temp < temp_green_max:
                    symbol = "🟢"  # Green circle
                elif temp < temp_red_min:
                    symbol = "🟡"  # Yellow/Amber circle
                else:
                    symbol = "🔴"  # Red circle
                self.indicator.set_label(f"{symbol} {label_text}", "")

            # Log status
            print(f"[TempIcon] {display_temp:.1f}{unit} - {status}")
            sys.stdout.flush()
        else:
            print("[TempIcon] ERROR: No sensor data")
            sys.stdout.flush()

        # Schedule next update
        interval = self.config_manager.get("update_interval", 5)
        self.update_timeout = GLib.timeout_add_seconds(
            interval, self._update_temperature
        )

        return False  # Don't call again from this callback

    def _on_settings_clicked(self, widget):
        """Handle settings menu click."""
        dialog = SettingsDialog(self.window, self.config_manager)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            settings = dialog.get_settings()

            # Update config
            for key, value in settings.items():
                self.config_manager.set(key, value)

            # Restart update loop with new interval
            if self.update_timeout:
                GLib.source_remove(self.update_timeout)
            self._update_temperature()

        dialog.destroy()

    def _on_tray_quit(self, widget=None):
        """Handle tray quit."""
        self.quit()
        return True

    def quit(self):
        """Quit the application."""
        print("[TempIcon] Shutting down...")
        sys.stdout.flush()

        if self.update_timeout:
            GLib.source_remove(self.update_timeout)

        Gtk.main_quit()


def main():
    """Entry point for the application."""
    app = TempIconApp()
    app.run()


if __name__ == "__main__":
    main()
