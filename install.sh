#!/bin/bash

set -e

echo "=== TempIcon Installer ==="
echo ""

# Check if running on Ubuntu
if ! grep -q "Ubuntu" /etc/os-release 2>/dev/null; then
    echo "Warning: This script is designed for Ubuntu. Your system may not be fully compatible."
fi

# Check Python3 installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install it first."
    exit 1
fi

echo "Step 1: Installing dependencies..."

# Update package manager
sudo apt-get update -qq

# Install required packages
sudo apt-get install -y \
    python3-gi \
    gir1.2-appindicator3-0.1 \
    lm-sensors \
    python3-pip

# Install Python packages
echo "Step 2: Installing Python dependencies..."
pip3 install --user psutil dbus-python

echo "Step 3: Setting up application files..."

# Create installation directory
INSTALL_DIR="$HOME/.local/share/tempicon"
mkdir -p "$INSTALL_DIR"

# Copy application files
cp -v src/*.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/temp_monitor.py"

# Create symlink for easy execution
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/temp_monitor.py" "$HOME/.local/bin/tempicon" || true

echo "Step 4: Setting up systemd service..."

# Create systemd user service directory
mkdir -p "$HOME/.config/systemd/user"

# Copy and customize service file
SERVICE_FILE="$HOME/.config/systemd/user/tempicon.service"
cp systemd/tempicon.service "$SERVICE_FILE"

# Reload systemd
systemctl --user daemon-reload

echo "Step 5: Enabling auto-start..."

# Enable service on boot
systemctl --user enable tempicon.service

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To start TempIcon now, run:"
echo "  systemctl --user start tempicon"
echo ""
echo "To view status:"
echo "  systemctl --user status tempicon"
echo ""
echo "To view logs:"
echo "  journalctl --user -u tempicon -f"
echo ""
echo "To open settings:"
echo "  Right-click the temperature indicator in the system tray"
echo ""
echo "To uninstall:"
echo "  systemctl --user stop tempicon"
echo "  systemctl --user disable tempicon"
echo "  rm -rf $INSTALL_DIR"
echo "  rm $HOME/.local/bin/tempicon"
echo ""
