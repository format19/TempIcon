"""Settings dialog for TempIcon application."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from config_manager import ConfigManager


class SettingsDialog(Gtk.Dialog):
    """Settings dialog for application configuration."""

    def __init__(self, parent_window, config_manager):
        """
        Initialize settings dialog.

        Args:
            parent_window: Parent window reference
            config_manager: ConfigManager instance
        """
        Gtk.Dialog.__init__(
            self,
            "TempIcon Settings",
            parent_window,
            Gtk.DialogFlags.MODAL,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
            ),
        )

        self.config_manager = config_manager
        self.set_default_size(400, 300)

        content_area = self.get_content_area()
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)

        # Create notebook tabs
        notebook = Gtk.Notebook()
        content_area.add(notebook)

        # General settings tab
        general_box = self._create_general_tab()
        notebook.append_page(general_box, Gtk.Label("General"))

        # About tab
        about_box = self._create_about_tab()
        notebook.append_page(about_box, Gtk.Label("About"))

        content_area.show_all()

    def _create_general_tab(self):
        """Create general settings tab."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        # Update interval
        interval_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        interval_label = Gtk.Label("Update Interval (seconds):")
        interval_label.set_xalign(0)
        interval_spin = Gtk.SpinButton()
        interval_spin.set_range(1, 60)
        interval_spin.set_value(self.config_manager.get("update_interval"))
        interval_spin.set_increments(1, 5)
        self.interval_spin = interval_spin

        interval_box.pack_start(interval_label, True, True, 0)
        interval_box.pack_end(interval_spin, False, False, 0)
        box.pack_start(interval_box, False, False, 0)

        # Temperature unit
        unit_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        unit_label = Gtk.Label("Temperature Unit:")
        unit_label.set_xalign(0)
        unit_combo = Gtk.ComboBoxText()
        unit_combo.append("celsius", "Celsius (°C)")
        unit_combo.append("fahrenheit", "Fahrenheit (°F)")

        show_f = self.config_manager.get("show_fahrenheit", False)
        unit_combo.set_active_id("fahrenheit" if show_f else "celsius")
        self.unit_combo = unit_combo

        unit_box.pack_start(unit_label, True, True, 0)
        unit_box.pack_end(unit_combo, False, False, 0)
        box.pack_start(unit_box, False, False, 0)

        # Icon style
        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        icon_label = Gtk.Label("Icon Style:")
        icon_label.set_xalign(0)
        icon_combo = Gtk.ComboBoxText()
        icon_combo.append("square", "Colored Square")
        icon_combo.append("circle", "Colored Circle")

        icon_style = self.config_manager.get("icon_style", "square")
        icon_combo.set_active_id(icon_style)
        self.icon_combo = icon_combo

        icon_box.pack_start(icon_label, True, True, 0)
        icon_box.pack_end(icon_combo, False, False, 0)
        box.pack_start(icon_box, False, False, 0)

        # Auto-start checkbox
        auto_start_check = Gtk.CheckButton("Auto-start on login")
        auto_start_check.set_active(self.config_manager.get("auto_start", True))
        self.auto_start_check = auto_start_check
        box.pack_start(auto_start_check, False, False, 0)

        # Temperature ranges section
        temp_label = Gtk.Label()
        temp_label.set_markup("<b>Temperature Thresholds (°C)</b>")
        temp_label.set_xalign(0)
        box.pack_start(temp_label, False, False, 0)

        # Green max threshold
        green_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        green_label = Gtk.Label("🟢 Green Below:")
        green_label.set_xalign(0)
        green_spin = Gtk.SpinButton()
        green_spin.set_range(20, 100)
        green_spin.set_value(self.config_manager.get("temp_green_max", 50))
        green_spin.set_increments(1, 5)
        self.green_spin = green_spin

        green_box.pack_start(green_label, True, True, 0)
        green_box.pack_end(green_spin, False, False, 0)
        box.pack_start(green_box, False, False, 0)

        # Red min threshold
        red_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        red_label = Gtk.Label("🔴 Red Above:")
        red_label.set_xalign(0)
        red_spin = Gtk.SpinButton()
        red_spin.set_range(30, 120)
        red_spin.set_value(self.config_manager.get("temp_red_min", 80))
        red_spin.set_increments(1, 5)
        self.red_spin = red_spin

        red_box.pack_start(red_label, True, True, 0)
        red_box.pack_end(red_spin, False, False, 0)
        box.pack_start(red_box, False, False, 0)

        # Info label
        info_label = Gtk.Label()
        info_label.set_markup(
            "<small>Amber is automatically between green and red thresholds</small>"
        )
        info_label.set_xalign(0)
        box.pack_start(info_label, False, False, 0)

        # Separator
        sep = Gtk.Separator()
        box.pack_start(sep, False, False, 0)

        # Reset button
        reset_button = Gtk.Button("Reset to Defaults")
        reset_button.connect("clicked", self._on_reset_clicked)
        box.pack_end(reset_button, False, False, 0)

        box.show_all()
        return box

    def _create_about_tab(self):
        """Create about tab."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        title = Gtk.Label()
        title.set_markup("<b>TempIcon</b>")
        title.set_xalign(0)
        box.pack_start(title, False, False, 0)

        version = Gtk.Label("Version 1.0.0")
        version.set_xalign(0)
        box.pack_start(version, False, False, 0)

        desc = Gtk.Label(
            "A GNOME system tray temperature monitor\n"
            "Displays CPU temperature with color coding:\n"
            "Green: < 50°C\n"
            "Amber: 50-80°C\n"
            "Red: > 80°C"
        )
        desc.set_xalign(0)
        desc.set_line_wrap(True)
        box.pack_start(desc, False, False, 0)

        box.show_all()
        return box

    def _on_reset_clicked(self, button):
        """Handle reset to defaults button click."""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Reset to Defaults?",
        )
        dialog.format_secondary_text(
            "This will reset all settings to their default values."
        )

        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            self.config_manager.reset_to_defaults()
            self.interval_spin.set_value(5)
            self.unit_combo.set_active_id("celsius")
            self.icon_combo.set_active_id("square")
            self.green_spin.set_value(50)
            self.red_spin.set_value(80)
            self.auto_start_check.set_active(True)

    def get_settings(self):
        """Get current settings from dialog."""
        return {
            "update_interval": int(self.interval_spin.get_value()),
            "show_fahrenheit": self.unit_combo.get_active_id() == "fahrenheit",
            "icon_style": self.icon_combo.get_active_id(),
            "temp_green_max": int(self.green_spin.get_value()),
            "temp_red_min": int(self.red_spin.get_value()),
            "auto_start": self.auto_start_check.get_active(),
        }
