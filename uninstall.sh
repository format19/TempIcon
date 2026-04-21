#!/bin/bash

# TempIcon Uninstaller
# Cleanly removes all TempIcon files and configurations

set -e

echo "=== TempIcon Uninstaller ==="
echo ""
echo "This will remove TempIcon and all its files."
echo ""
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Step 1: Stopping and disabling service..."

# Stop the service if running
systemctl --user stop tempicon 2>/dev/null || true

# Disable auto-start
systemctl --user disable tempicon 2>/dev/null || true

echo "✓ Service stopped and disabled"

echo ""
echo "Step 2: Removing application files..."

# Remove application directory
if [ -d "$HOME/.local/share/tempicon" ]; then
    rm -rf "$HOME/.local/share/tempicon"
    echo "✓ Removed ~/.local/share/tempicon"
fi

# Remove symlink
if [ -L "$HOME/.local/bin/tempicon" ]; then
    rm "$HOME/.local/bin/tempicon"
    echo "✓ Removed ~/.local/bin/tempicon symlink"
fi

echo ""
echo "Step 3: Removing systemd service file..."

# Remove service file
if [ -f "$HOME/.config/systemd/user/tempicon.service" ]; then
    rm "$HOME/.config/systemd/user/tempicon.service"
    echo "✓ Removed ~/.config/systemd/user/tempicon.service"
fi

# Reload systemd daemon
systemctl --user daemon-reload
echo "✓ Reloaded systemd"

echo ""
echo "Step 4: Removing configuration files..."

# Remove config directory
if [ -d "$HOME/.config/tempicon" ]; then
    rm -rf "$HOME/.config/tempicon"
    echo "✓ Removed ~/.config/tempicon"
fi

echo ""
echo "=== Uninstallation Complete ==="
echo ""
echo "All TempIcon files and configurations have been removed."
echo ""
