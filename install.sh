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

echo "Step 1: Installing system dependencies..."

# Update package manager
sudo apt-get update -qq

# Install required system packages
sudo apt-get install -y \
    python3-gi \
    python3-venv \
    gir1.2-appindicator3-0.1 \
    gir1.2-gtk-3.0 \
    gir1.2-glib-2.0 \
    lm-sensors

echo "Step 2: Creating Python virtual environment..."

# Get the directory where the script is located (project root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"

# Create virtual environment with system site packages
# This allows access to system-installed gi module (PyGObject)
python3 -m venv "$VENV_DIR" --system-site-packages

echo "Step 3: Installing Python dependencies..."

# Install requirements using the venv's pip
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

echo "Step 4: Setting up application files..."

# Create installation directory
INSTALL_DIR="$HOME/.local/share/tempicon"
mkdir -p "$INSTALL_DIR"

# Copy application files
cp -v "$SCRIPT_DIR/src"/*.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/temp_monitor.py"

# Copy the venv to the install directory
cp -r "$VENV_DIR" "$INSTALL_DIR/"

echo "Step 5: Creating launcher script..."

# Create a wrapper script that uses the venv
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/tempicon" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/tempicon"
exec "$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/temp_monitor.py"
EOF
chmod +x "$HOME/.local/bin/tempicon"

echo "Step 6: Creating autostart .desktop file..."

# Create autostart directory
mkdir -p "$HOME/.config/autostart"

# Create desktop file for autostart
cat > "$HOME/.config/autostart/tempicon.desktop" << EOF
[Desktop Entry]
Type=Application
Name=TempIcon
Comment=Temperature indicator for system tray
Exec=$HOME/.local/bin/tempicon
Icon=utilities-system-monitor
Categories=System;Utility;
X-GNOME-Autostart-enabled=true
Hidden=false
EOF

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To start TempIcon now, run:"
echo "  $HOME/.local/bin/tempicon"
echo ""
echo "TempIcon will automatically start on your next login."
echo ""
echo "To view the application:"
echo "  Look for the temperature indicator in the system tray"
echo ""
echo "To open settings:"
echo "  Right-click the temperature indicator in the system tray"
echo ""
echo "To uninstall:"
echo "  rm -rf $INSTALL_DIR"
echo "  rm $HOME/.local/bin/tempicon"
echo "  rm $HOME/.config/autostart/tempicon.desktop"
echo ""
