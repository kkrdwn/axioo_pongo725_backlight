#!/usr/bin/env python3
import gi
import os
import sys
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

KBD_PATH = "/sys/devices/platform/tuxedo_keyboard/leds/rgb:kbd_backlight"
PRESET_COLORS = {
    "Merah": (255, 0, 0),
    "Hijau": (0, 255, 0),
    "Biru": (0, 0, 255),
    "Putih": (255, 255, 255),
    "Off": (0, 0, 0)
}

def set_kbd_backlight(brightness, rgb):
    try:
        with open(os.path.join(KBD_PATH, "brightness"), "w") as f:
            f.write(str(int(brightness)))
        with open(os.path.join(KBD_PATH, "multi_intensity"), "w") as f:
            f.write(f"{rgb[0]} {rgb[1]} {rgb[2]}")
        return True, ""
    except Exception as e:
        return False, str(e)

def main():
    # Jika dipanggil dengan argumen khusus, jalankan mode helper root
    if len(sys.argv) == 4 and sys.argv[1] == "--set-backlight":
        brightness = sys.argv[2]
        rgb = sys.argv[3].split(',')
        ok, err = set_kbd_backlight(brightness, rgb)
        if ok:
            sys.exit(0)
        else:
            print(f"Failed: {err}")
            sys.exit(2)

class KeyboardBacklightGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Keyboard Backlight Control")
        self.set_border_width(10)
        self.set_default_size(350, 200)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Brightness slider
        self.brightness = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=Gtk.Adjustment(value=128, lower=0, upper=255, step_increment=1, page_increment=10, page_size=0)
        )
        self.brightness.set_digits(0)
        
        self.brightness.set_value_pos(Gtk.PositionType.RIGHT)
        vbox.pack_start(Gtk.Label(label="Brightness"), False, False, 0)
        vbox.pack_start(self.brightness, False, False, 0)

        # Color buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.pack_start(Gtk.Label(label="Preset Warna"), False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        self.selected_rgb = PRESET_COLORS["Putih"]
        for name, rgb in PRESET_COLORS.items():
            btn = Gtk.Button(label=name)
            btn.connect("clicked", self.on_color_clicked, rgb)
            hbox.pack_start(btn, True, True, 0)

        # Apply button
        apply_btn = Gtk.Button(label="Apply")
        apply_btn.connect("clicked", self.on_apply_clicked)
        vbox.pack_end(apply_btn, False, False, 0)

    def on_color_clicked(self, button, rgb):
        self.selected_rgb = rgb

    def on_apply_clicked(self, button):
        brightness = int(self.brightness.get_value())
        rgb = self.selected_rgb
        ok, err = set_kbd_backlight(brightness, rgb)
        if ok:
            self.show_info("Backlight updated!")
            return
        # Jika gagal permission, coba pkexec panggil script ini sendiri
        try:
            rgb_str = f"{rgb[0]},{rgb[1]},{rgb[2]}"
            script_path = os.path.abspath(sys.argv[0])
            result = subprocess.run(
                ["pkexec", "python3", script_path, "--set-backlight", str(brightness), rgb_str],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.show_info("Backlight updated (via pkexec)!")
            else:
                self.show_error(f"pkexec failed: {result.stderr or result.stdout}")
        except Exception as e:
            self.show_error(f"Failed to set backlight (pkexec): {e}")

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text="Error"
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def show_info(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Info"
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    # Mode helper root jika dipanggil dengan argumen khusus
    main()
    # Jika tidak, jalankan GUI
    win = KeyboardBacklightGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
