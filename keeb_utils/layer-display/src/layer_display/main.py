"""Main menubar application."""

import os
import rumps
from .keyboard_hid import KeyboardHIDListener, MOON_KNIGHT_VID, MOON_KNIGHT_PID
from .vial_parser import VialKeymapParser


class LayerDisplayApp(rumps.App):
    """macOS menubar app to display keyboard layer."""

    # Layer names matching your keymap
    LAYER_NAMES = {
        0: "Base",
        1: "Numbers",
        2: "Symbols",
        3: "Function",
    }

    def __init__(self, vial_file: str = None):
        super(LayerDisplayApp, self).__init__(
            "❌",  # Initial menubar text (disconnected)
            quit_button="Quit"
        )

        self.current_layer = None
        self.hid_listener = None
        self.keymap_parser = None
        self.status_item = None

        # Try to load Vial keymap if provided
        if vial_file and os.path.exists(vial_file):
            try:
                self.keymap_parser = VialKeymapParser(vial_file)
                print(f"Loaded keymap from {vial_file}")
            except Exception as e:
                print(f"Failed to load Vial keymap: {e}")

        # Build menu
        self._build_menu()

        # Try to connect to keyboard
        self._connect_keyboard()

    def _build_menu(self):
        """Build the menubar menu structure."""
        self.menu.clear()

        # Status item with callback
        self.status_item = rumps.MenuItem("Status: Connecting...", callback=self._on_status_click)
        self.menu.add(self.status_item)
        self.menu.add(rumps.separator)

        # Layer items with keymaps
        for i in range(4):
            layer_name = self.LAYER_NAMES[i]
            layer_item = rumps.MenuItem(f"Layer {i} - {layer_name}", callback=None)

            if self.keymap_parser:
                # Add keymap as submenu
                keymap_ascii = self.keymap_parser.format_layer_ascii(i)
                # Split into lines and add as menu items
                for line in keymap_ascii.split("\n"):
                    if line.strip():
                        layer_item.add(rumps.MenuItem(line, callback=None))

            self.menu.add(layer_item)

    def _connect_keyboard(self):
        """Attempt to connect to the keyboard via HID."""
        try:
            self.hid_listener = KeyboardHIDListener(
                vendor_id=MOON_KNIGHT_VID,
                product_id=MOON_KNIGHT_PID,
                on_layer_change=self._on_layer_change
            )

            if self.hid_listener.connect():
                self.hid_listener.start()
                self.status_item.title = "Status: Connected ✓"
                # Set initial layer to 0
                self._on_layer_change(0)
            else:
                self.status_item.title = "Status: Not found (check USB)"

        except Exception as e:
            print(f"Failed to connect to keyboard: {e}")
            self.status_item.title = f"Status: Error - {e}"

    def _on_layer_change(self, layer: int):
        """Called when keyboard layer changes."""
        self.current_layer = layer
        layer_name = self.LAYER_NAMES.get(layer, f"Unknown ({layer})")

        # Update menubar text (short format)
        self.title = f"L{layer}"

        # Highlight current layer in menu
        for i in range(4):
            menu_item = self.menu[f"Layer {i} - {self.LAYER_NAMES[i]}"]
            if i == layer:
                menu_item.state = 1  # Checkmark
            else:
                menu_item.state = 0

    def _on_status_click(self, sender):
        """Handle click on status item to reconnect."""
        sender.title = "Status: Reconnecting..."
        self._connect_keyboard()


def main():
    """Entry point for the application."""
    import sys
    from pathlib import Path

    # Look for vial.vil in common locations
    vial_file = None
    search_paths = [
        Path.home() / "Desktop" / "vial.vil",
        Path.home() / "Desktop" / "moon_knight_kbd" / "firmwares" / "dj" / "moon_knight" / "moon_knight_vial_backup.vil",
    ]

    for path in search_paths:
        if path.exists():
            vial_file = str(path)
            break

    if vial_file:
        print(f"Found Vial keymap: {vial_file}")
    else:
        print("No Vial keymap found, running without keymap display")

    app = LayerDisplayApp(vial_file=vial_file)
    app.run()


if __name__ == "__main__":
    main()
