#!/bin/bash
set -e

echo "🔧 Building SD Card Formatter DEB Package..."

DEB_DIR="sdcard-formatter_1.0.0"
ICON_PATH="../SD-Card-Formatter-Linux-GTK3-GUI-/sdcard-formatter-installer/icons/sdcard-formatter.png"

# Copy GUI script
echo "📋 Copying GUI script..."
cp ../sdcard-formatter-appimage/sd_formatter_gui.py "$DEB_DIR/usr/local/bin/"
chmod +x "$DEB_DIR/usr/local/bin/sd_formatter_gui.py"

# Copy format_sd binary
echo "📋 Copying format_sd binary..."
cp /usr/local/bin/format_sd "$DEB_DIR/usr/local/bin/"
chmod +x "$DEB_DIR/usr/local/bin/format_sd"

# Copy icon
if [ -f "$ICON_PATH" ]; then
    echo "🎨 Copying icon..."
    cp "$ICON_PATH" "$DEB_DIR/usr/share/icons/hicolor/256x256/apps/sdcard-formatter.png"
fi

# Set permissions
echo "🔧 Setting permissions..."
chmod 755 "$DEB_DIR/DEBIAN"
chmod 644 "$DEB_DIR/DEBIAN/control"

# Build DEB package
echo "📦 Building DEB package..."
dpkg-deb --build --root-owner-group "$DEB_DIR"

# Move to current directory
mv "$DEB_DIR.deb" .

echo "✅ DEB package created: sdcard-formatter_1.0.0.deb"
echo ""
echo "Installation:"
echo "  sudo dpkg -i sdcard-formatter_1.0.0.deb"
echo "  sudo apt-get install -f  # Install missing dependencies if any"
echo ""
echo "Uninstall:"
echo "  sudo dpkg -r sdcard-formatter"
