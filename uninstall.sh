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
echo "Step 1: Removing application files..."

# Remove application directory
if [ -d "$HOME/.local/share/tempicon" ]; then
    rm -rf "$HOME/.local/share/tempicon"
    echo "✓ Removed ~/.local/share/tempicon"
fi

# Remove launcher script
if [ -f "$HOME/.local/bin/tempicon" ]; then
    rm "$HOME/.local/bin/tempicon"
    echo "✓ Removed ~/.local/bin/tempicon"
fi

echo ""
echo "Step 2: Removing autostart configuration..."

# Remove desktop file
if [ -f "$HOME/.config/autostart/tempicon.desktop" ]; then
    rm "$HOME/.config/autostart/tempicon.desktop"
    echo "✓ Removed ~/.config/autostart/tempicon.desktop"
fi

echo ""
echo "Step 3: Removing configuration files..."

# Remove config directory (optional - user can keep their settings)
read -p "Remove configuration files? (yes/no): " remove_config

if [ "$remove_config" = "yes" ]; then
    if [ -d "$HOME/.config/tempicon" ]; then
        rm -rf "$HOME/.config/tempicon"
        echo "✓ Removed ~/.config/tempicon"
    fi
else
    echo "✓ Kept ~/.config/tempicon (configuration preserved)"
fi

echo ""
echo "=== Uninstallation Complete ==="
echo ""
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
