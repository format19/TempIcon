# TempIcon - Lightweight CPU Temperature Monitor for GNOME

A minimal system tray application that monitors your CPU temperature in real-time with color-coded visual indicators. Runs as a background service with automatic startup.

---

## ✨ Features

- **Real-time Temperature Display** - CPU temperature updated every 5 seconds in the system tray
- **Color-Coded Indicators** (fully customizable):
  - 🟢 **Green** - Optimal temperature (default: < 50°C)
  - 🟡 **Amber** - Warm temperature (default: 50-80°C)  
  - 🔴 **Red** - Hot temperature (default: > 80°C)
- **Icon Styles** - Display as colored square or circle with temperature number
- **Temperature Units** - Toggle between Celsius and Fahrenheit
- **Configurable Thresholds** - Set your own temperature ranges for color changes
- **Auto-refresh** - Updates configurable from 1-60 seconds (default: 5 seconds)
- **Settings UI** - Right-click menu for easy configuration
- **Auto-start** - System service runs automatically on login
- **Lightweight** - Minimal resource usage (~20MB memory)
- **Error Handling** - Gracefully handles missing sensors

---

## 🔧 Requirements

- **OS**: Ubuntu 24.04 (or similar GNOME-based Linux distribution)
- **Python**: 3.8 or higher
- **Hardware**: System with CPU temperature sensors (hwmon or lm-sensors)
- **Desktop**: GNOME or GNOME-compatible environment

---

## 📦 Installation

### Quick Install

```bash
cd TempIcon
chmod +x install.sh
./install.sh
```

The installer will:
- Install system dependencies (Python libraries, lm-sensors)
- Copy application files to `~/.local/share/tempicon/`
- Register and enable systemd user service for auto-start
- Create a convenient symlink in `~/.local/bin/`

### Manual Installation

If you prefer to set up manually:

1. **Install system dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-gi gir1.2-appindicator3-0.1 lm-sensors python3-pip
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install --user -r requirements.txt
   ```

3. **Copy application files**:
   ```bash
   mkdir -p ~/.local/share/tempicon
   cp src/*.py ~/.local/share/tempicon/
   chmod +x ~/.local/share/tempicon/temp_monitor.py
   ```

4. **Setup systemd service**:
   ```bash
   mkdir -p ~/.config/systemd/user
   cp systemd/tempicon.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable tempicon.service
   systemctl --user start tempicon
   ```

---

## 🚀 Usage

### Start the Service

```bash
# Start the service
systemctl --user start tempicon

# Or run directly from command line
python3 ~/.local/share/tempicon/temp_monitor.py
```

### Configure Settings

Right-click on the temperature indicator in the system tray to access the menu:
- **Settings** - Adjust update interval, temperature units, icon style, and thresholds
- **Quit** - Stop the application

### View Logs

```bash
# Stream logs in real-time
journalctl --user -u tempicon -f

# View last 50 log lines
journalctl --user -u tempicon -n 50

# View logs since last boot
journalctl --user -u tempicon --since today
```

### Check Service Status

```bash
systemctl --user status tempicon
```

---

## 🛠️ Uninstallation

To completely remove TempIcon and all its files:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

Or manually:

```bash
# Stop and disable the service
systemctl --user stop tempicon
systemctl --user disable tempicon

# Remove application files
rm -rf ~/.local/share/tempicon
rm ~/.local/bin/tempicon 2>/dev/null || true

# Remove service file
rm ~/.config/systemd/user/tempicon.service
systemctl --user daemon-reload

# Remove configuration
rm -rf ~/.config/tempicon
```

---

## 🔧 Configuration

Settings are stored in `~/.config/tempicon/config.json` and can be edited manually or through the Settings dialog:

```json
{
  "update_interval": 5,
  "show_fahrenheit": false,
  "icon_style": "square",
  "temp_green_max": 50,
  "temp_red_min": 80,
  "auto_start": true
}
```

**Configuration Options:**
- `update_interval` (1-60): Seconds between temperature updates
- `show_fahrenheit` (true/false): Display temperature in Fahrenheit
- `icon_style` ("square" or "circle"): Visual style of the tray indicator
- `temp_green_max`: Temperature threshold for green status (°C)
- `temp_red_min`: Temperature threshold for red status (°C)
- `auto_start` (true/false): Enable auto-start on login

---

## 🐛 Troubleshooting

### Application doesn't appear in system tray

Check that the service is running:
```bash
systemctl --user status tempicon
```

View logs for errors:
```bash
journalctl --user -u tempicon -f
```

Ensure you're using GNOME or a compatible desktop environment.

### "No sensor data" error

The system can't find temperature sensors. Try:

```bash
# Check available sensors
sensors

# Install additional sensor drivers
sudo apt-get install lm-sensors
sudo sensors-detect  # Follow the prompts
```

### CPU temperature seems wrong

Check your actual sensor data:
```bash
sensors

# Or check hwmon directly
cat /sys/class/hwmon/hwmon*/temp*_input
```

### High memory usage

This is typically due to GTK initialization. Memory should stabilize around 20-25MB after startup.

---

## 📋 Project Structure

```
TempIcon/
├── src/                          # Python source code
│   ├── temp_monitor.py          # Main application controller
│   ├── temp_reader.py           # CPU temperature sensor interface
│   ├── config_manager.py        # Settings persistence
│   ├── settings_dialog.py       # GTK configuration UI
│   └── icon_generator.py        # SVG icon generation (reserved)
├── systemd/                      # Service configuration
│   └── tempicon.service         # Systemd user service file
├── install.sh                    # Installation script
├── uninstall.sh                  # Uninstallation script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 💻 Development

### Run from source
```bash
cd TempIcon
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/temp_monitor.py
```

### Code Style
- Clean, readable Python code
- Minimal dependencies
- Focus on reliability and low resource usage

---

## 📝 License

This project is provided as-is. Feel free to modify and distribute.

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional temperature sensor support
- Support for other desktop environments
- Performance optimizations
- Additional icon styles or themes

---

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review systemd logs: `journalctl --user -u tempicon -f`
3. Verify sensor availability: `sensors`

---

**Happy monitoring!** 🌡️
