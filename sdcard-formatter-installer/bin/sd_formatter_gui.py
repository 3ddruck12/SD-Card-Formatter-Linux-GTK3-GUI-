#!/usr/bin/env python3

import gi
import subprocess
import os
import re
import sys
import tarfile
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FirstRunDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Setup Required", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        
        self.set_default_size(500, 300)
        self.set_resizable(False)
        self.selected_file = None
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        
        # Warning icon
        warning_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        warning_icon = Gtk.Image.new_from_icon_name("dialog-warning", Gtk.IconSize.DIALOG)
        warning_box.pack_start(warning_icon, False, False, 0)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup("<big><b>format_sd Binary Required</b></big>")
        warning_box.pack_start(title_label, False, False, 0)
        box.pack_start(warning_box, False, False, 10)
        
        # Explanation
        explanation = Gtk.Label()
        explanation.set_markup(
            "The official <b>format_sd</b> binary from Tuxera is required but not found.\n\n"
            "Due to licensing restrictions, this file cannot be included in the application.\n"
            "Please download it from the official website:"
        )
        explanation.set_line_wrap(True)
        explanation.set_xalign(0)
        box.pack_start(explanation, False, False, 0)
        
        # Download link button
        link_button = Gtk.LinkButton.new_with_label(
            "https://www.sdcard.org/downloads/sd-memory-card-formatter-for-linux/",
            "🔗 Download SDCardFormatterv1.0.3_Linux_x86_64.tgz"
        )
        box.pack_start(link_button, False, False, 0)
        
        # Instructions
        instructions = Gtk.Label()
        instructions.set_markup(
            "\n<b>Steps:</b>\n"
            "1. Click the link above to download the .tgz file\n"
            "2. Click 'Select Downloaded File' below\n"
            "3. Choose the downloaded .tgz file"
        )
        instructions.set_line_wrap(True)
        instructions.set_xalign(0)
        box.pack_start(instructions, False, False, 0)
        
        # File chooser button
        file_button = Gtk.Button(label="📁 Select Downloaded File")
        file_button.connect("clicked", self.on_file_select)
        box.pack_start(file_button, False, False, 10)
        
        # Status label
        self.status_label = Gtk.Label()
        self.status_label.set_line_wrap(True)
        box.pack_start(self.status_label, False, False, 0)
        
        # OK button (initially disabled)
        self.ok_button = self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.ok_button.set_sensitive(False)
        
        self.show_all()
    
    def on_file_select(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select SDCardFormatterv1.0.3_Linux_x86_64.tgz",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        # Add file filter
        filter_tgz = Gtk.FileFilter()
        filter_tgz.set_name("TGZ files")
        filter_tgz.add_pattern("*.tgz")
        filter_tgz.add_pattern("*.tar.gz")
        dialog.add_filter(filter_tgz)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.selected_file = dialog.get_filename()
            self.status_label.set_markup(f"<span color='blue'>Selected: {os.path.basename(self.selected_file)}</span>")
            
            # Try to extract and verify
            if self.extract_format_sd():
                self.status_label.set_markup("<span color='green'>✓ format_sd extracted successfully!</span>")
                self.ok_button.set_sensitive(True)
            else:
                self.status_label.set_markup("<span color='red'>✗ Could not find format_sd in archive</span>")
                self.ok_button.set_sensitive(False)
        
        dialog.destroy()
    
    def extract_format_sd(self):
        try:
            # Create temp directory for extraction
            temp_dir = "/tmp/sdcard_formatter_extract"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extract tar.gz
            with tarfile.open(self.selected_file, 'r:gz') as tar:
                tar.extractall(temp_dir)
            
            # Find format_sd binary
            format_sd_path = None
            for root, dirs, files in os.walk(temp_dir):
                if 'format_sd' in files:
                    format_sd_path = os.path.join(root, 'format_sd')
                    break
            
            if not format_sd_path:
                return False
            
            # Determine installation path
            install_paths = [
                os.path.expanduser("~/.sd/format_sd"),
                "/usr/local/bin/format_sd"
            ]
            
            # Try to copy to ~/.sd first (no sudo needed)
            local_bin = os.path.expanduser("~/.sd")
            os.makedirs(local_bin, exist_ok=True)
            dest_path = os.path.join(local_bin, "format_sd")
            
            shutil.copy2(format_sd_path, dest_path)
            os.chmod(dest_path, 0o755)
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            return True
            
        except Exception as e:
            print(f"Error extracting format_sd: {e}")
            return False

class SDFormatter(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="SD Card Formatter (Unofficial Community Project)")
        self.set_border_width(10)
        self.set_default_size(420, 320)
        self.set_resizable(False)

        # Set window/taskbar icon
        icon_path = os.path.expanduser("~/.local/share/icons/sdcard-formatter.png")
        if os.path.exists(icon_path):
            self.set_icon_from_file(icon_path)

        # GUI Layout
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        # Top image
        if os.path.exists(icon_path):
            image = Gtk.Image.new_from_file(icon_path)
            grid.attach(image, 0, 0, 3, 1)

        # Device dropdown
        grid.attach(Gtk.Label(label="Select Device:"), 0, 1, 1, 1)
        self.device_dropdown = Gtk.ComboBoxText()
        grid.attach(self.device_dropdown, 1, 1, 1, 1)

        self.refresh_button = Gtk.Button(label="🔄 Refresh")
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
        grid.attach(self.refresh_button, 2, 1, 1, 1)

        # Volume Label
        grid.attach(Gtk.Label(label="Volume Label:"), 0, 2, 1, 1)
        self.label_entry = Gtk.Entry()
        self.label_entry.set_max_length(11)
        grid.attach(self.label_entry, 1, 2, 2, 1)

        # Format Type
        grid.attach(Gtk.Label(label="Format Type:"), 0, 3, 1, 1)
        self.format_type = Gtk.ComboBoxText()
        self.format_type.append_text("Quick (Default)")
        self.format_type.append_text("Discard")
        self.format_type.append_text("Overwrite")
        self.format_type.set_active(0)
        grid.attach(self.format_type, 1, 3, 2, 1)

        # Format Button
        self.format_button = Gtk.Button(label="Format")
        self.format_button.connect("clicked", self.on_format_clicked)
        grid.attach(self.format_button, 1, 4, 1, 1)

        # Output Label
        self.output_label = Gtk.Label(label="")
        self.output_label.set_line_wrap(True)
        grid.attach(self.output_label, 0, 5, 3, 2)

        # Load devices initially
        self.populate_devices()

    def check_format_sd(self):
        """Check if format_sd binary exists"""
        paths = [
            os.path.expanduser("~/.sd/format_sd"),
            "/usr/local/bin/format_sd",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "format_sd")
        ]
        
        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return True
        return False

    def get_format_sd_path(self):
        """Get the path to format_sd binary"""
        paths = [
            os.path.expanduser("~/.sd/format_sd"),
            "/usr/local/bin/format_sd",
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "format_sd")
        ]
        
        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        return None

    def populate_devices(self):
        self.device_dropdown.remove_all()
        try:
            output = subprocess.check_output(
                ["lsblk", "-P", "-o", "NAME,SIZE,TYPE,RM,TRAN,MODEL"],
                text=True
            )
            print("DEBUG: lsblk -P output:\n", output)

            for line in output.strip().split('\n'):
                info = dict(re.findall(r'(\w+)="([^"]*)"', line))
                print("DEBUG LINE PARSED:", info)

                if info.get("TYPE") == "disk" and (info.get("RM") == "1" or info.get("TRAN") == "mmc"):
                    name = info["NAME"]
                    size = info["SIZE"]
                    model = info.get("MODEL", "")
                    device_path = f"/dev/{name}"
                    label = f"{device_path} – {size} – {model or 'Removable'}"
                    print("DEBUG ADDING:", label)
                    self.device_dropdown.append_text(label)

            if self.device_dropdown.get_active() == -1:
                self.device_dropdown.set_active(0)

        except Exception as e:
            self.output_label.set_text(f"Device detection error: {e}")
            print("DEBUG ERROR:", e)

    def on_refresh_clicked(self, widget):
        self.populate_devices()
        self.output_label.set_text("🔄 Device list refreshed.")

    def on_format_clicked(self, widget):
        selected_text = self.device_dropdown.get_active_text()
        label = self.label_entry.get_text().strip()
        mode = self.format_type.get_active_text()

        if not selected_text:
            self.output_label.set_text("❌ No device selected.")
            return

        device = selected_text.split("–")[0].strip()
        if not os.path.exists(device):
            self.output_label.set_text("❌ Device path does not exist.")
            return

        # 🔒 Confirm formatting
        confirm_dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=f"⚠️ Are you sure you want to format {device}?",
        )
        confirm_dialog.format_secondary_text("All data on this device will be permanently lost.")
        confirm_dialog.set_title("Confirm Format")
        response = confirm_dialog.run()
        confirm_dialog.destroy()

        if response != Gtk.ResponseType.OK:
            self.output_label.set_text("❎ Format cancelled.")
            return

        # 🔌 Unmount all partitions
        try:
            lsblk_output = subprocess.check_output(["lsblk", "-ln", "-o", "NAME", device], text=True)
            partitions = lsblk_output.strip().split("\n")[1:]  # skip the device itself

            for part in partitions:
                part_path = f"/dev/{part}"
                subprocess.run(["udisksctl", "unmount", "-b", part_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Unmounted {part_path}")
        except Exception as e:
            print(f"Unmount failed: {e}")

        # Format command (no pkexec needed if already running as root)
        format_sd_path = self.get_format_sd_path()
        cmd = [format_sd_path, "-l", label or "Untitled"]
        if mode == "Discard":
            cmd.append("--discard")
        elif mode == "Overwrite":
            cmd.append("--overwrite")
        cmd.append(device)

        try:
            self.output_label.set_text("⚙️ Formatting in progress...")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().splitlines()
                self.output_label.set_text("✅ Success:\n" + (lines[-1] if lines else "Done."))
            else:
                self.output_label.set_text("❌ Error:\n" + result.stderr.strip())
        except Exception as e:
            self.output_label.set_text(f"⚠️ Exception: {e}")
            print("DEBUG ERROR:", e)

def show_first_run_dialog_if_needed():
    """Check and show first-run dialog if format_sd is missing"""
    paths = [
        os.path.expanduser("~/.sd/format_sd"),
        "/usr/local/bin/format_sd"
    ]
    
    format_sd_exists = any(os.path.exists(p) and os.access(p, os.X_OK) for p in paths)
    
    if not format_sd_exists:
        dialog = FirstRunDialog(None)
        response = dialog.run()
        dialog.destroy()
        
        # Check again after dialog
        format_sd_exists = any(os.path.exists(p) and os.access(p, os.X_OK) for p in paths)
        
        if response != Gtk.ResponseType.OK or not format_sd_exists:
            error_dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Cannot continue without format_sd",
            )
            error_dialog.format_secondary_text(
                "The application cannot function without the format_sd binary."
            )
            error_dialog.run()
            error_dialog.destroy()
            return False
    
    return True

if __name__ == "__main__":
    # Check if running as root, if not restart with pkexec
    if False and os.geteuid() != 0:
        print("Not running as root, restarting with pkexec...")
        try:
            # Restart with pkexec
            os.execvp("pkexec", ["pkexec", sys.executable] + sys.argv)
        except Exception as e:
            print(f"Failed to elevate privileges: {e}")
            sys.exit(1)
    
    # Show first-run dialog before creating main window
    if not show_first_run_dialog_if_needed():
        sys.exit(1)
    
    win = SDFormatter()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
