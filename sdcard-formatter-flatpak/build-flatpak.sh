#!/bin/bash
set -e

echo "🔧 Building SD Card Formatter Flatpak..."

# Check if flatpak-builder is installed
if ! command -v flatpak-builder &> /dev/null; then
    echo "❌ flatpak-builder not found. Install it with:"
    echo "   sudo apt install flatpak-builder"
    exit 1
fi

# Check if Freedesktop runtime is installed
if ! flatpak list --runtime | grep -q "org.freedesktop.Platform.*23.08"; then
    echo "📦 Installing Freedesktop runtime..."
    flatpak install -y flathub org.freedesktop.Platform//23.08 org.freedesktop.Sdk//23.08
fi

# Build the Flatpak
echo "🔨 Building Flatpak package..."
flatpak-builder --force-clean --install --user build-dir org.sdcard.Formatter.yaml

echo "✅ Flatpak built and installed!"
echo ""
echo "Run with:"
echo "  flatpak run org.sdcard.Formatter"
echo ""
echo "Create bundle:"
echo "  flatpak build-bundle ~/.local/share/flatpak/repo SDCardFormatter.flatpak org.sdcard.Formatter"
