# SD Card Formatter (Linux GTK3 GUI)

<p align="center">
  <img src="https://raw.githubusercontent.com/Stradios/SD-Card-Formatter-Linux-GTK3-GUI-/refs/heads/main/Screenshot%20From%202025-08-04%2022-37-59.png" alt="Screenshot">
</p>

---

This project provides a GTK3 front-end for [Tuxera's official SD Card Formatter](https://www.sdcard.org/downloads/sd-memory-card-formatter-for-linux/).  
> ⚠️ Due to licensing restrictions, you **must manually download** the binary `format_sd`.

**New:** We've added a first-run setup window that simplifies the download process and guides you through the initial setup.

**Available as DEB and Flatpak packages** - Check [Releases](https://github.com/3ddruck12/SD-Card-Formatter-Linux-GTK3-GUI-/releases) for pre-built packages!

---

## 📦 Installation

### Option 1: DEB Package (Debian/Ubuntu)

1. Download `sdcard-formatter_1.0.0.deb` from [Releases](https://github.com/3ddruck12/SD-Card-Formatter-Linux-GTK3-GUI-/releases)
2. Install the package:

```bash
sudo dpkg -i sdcard-formatter_1.0.0.deb
sudo apt-get install -f  # Install dependencies if needed
```

3. Run from application menu or terminal:
```bash
sd_formatter_gui.py
```

### Option 2: Flatpak (Universal)

1. Download `sdcard-formatter.flatpak` from [Releases](https://github.com/3ddruck12/SD-Card-Formatter-Linux-GTK3-GUI-/releases)
2. Install the package:

```bash
flatpak install sdcard-formatter.flatpak
```

3. Run the application:
```bash
flatpak run org.sdcard.Formatter
```

---


## 🖼 Features

- Simple GTK3 interface
- **First-run setup window** - Guides you through the download and setup process
- Available as **DEB and Flatpak** packages
- Lists only removable drives
- Choose Quick, Discard, or Overwrite format types
- Confirmation before formatting
- Shows output messages
- Detects and unmounts drives before formatting
- Desktop icon with taskbar support

---

## 📝 License

This GUI is open-source (MIT license).  
The **`format_sd` binary is proprietary** and must be downloaded from the official SD Association website.

---

## 🧊 Author

Developed by [Stradios](https://github.com/Stradios)
